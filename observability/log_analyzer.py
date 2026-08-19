"""Log analysis — derive counters, latency, and cost from the structured log file.

The observability stack writes every event as one JSON line to `ba_copilot.log`.
This module parses that file and derives everything from it, so the log is the
single source of truth (no separate metrics store).
"""

import json
from collections import defaultdict
from pathlib import Path

# Estimated pricing (USD per 1M tokens). Placeholder until real pricing is wired.
INPUT_COST_PER_1M = 0.14
OUTPUT_COST_PER_1M = 0.28


class LogAnalyzer:
    """Parse `ba_copilot.log` and derive counters, latency, and cost."""

    def __init__(self, log_file=None):
        self.log_file = log_file or Path(__file__).parent / "logs" / "ba_copilot.log"
        self.logs = []
        self.load_log()

    # ── Loading ─────────────────────────────────────────────────────────
    def load_log(self):
        """(Re)load all JSON log lines from the log file."""
        self.logs = []
        if not Path(self.log_file).exists():
            return []

        with open(self.log_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return self.logs

    # ── Latency ─────────────────────────────────────────────────────────
    def component_latency_stats(self):
        """Per-component duration stats: count, avg, min, max (ms)."""
        duration_map = defaultdict(list)
        for log in self.logs:
            component = log.get("component")
            duration_ms = log.get("duration_ms")
            if component and duration_ms is not None:
                duration_map[component].append(duration_ms)

        return {
            component: {
                "count": len(durations),
                "avg_ms": round(sum(durations) / len(durations), 2),
                "min_ms": round(min(durations), 2),
                "max_ms": round(max(durations), 2),
            }
            for component, durations in duration_map.items()
        }

    def slowest_component(self, exclude=("workflow",)):
        """Return (component, stats) with the highest avg_ms, excluding
        the 'workflow' total, which would otherwise always win."""
        stats = self.component_latency_stats()
        candidates = {c: s for c, s in stats.items() if c not in exclude}
        if not candidates:
            return None
        return max(candidates.items(), key=lambda item: item[1]["avg_ms"])

    # ── Counters ────────────────────────────────────────────────────────
    def _count(self, component=None, level=None, message_prefix=None):
        """Count log records matching optional filters."""
        total = 0
        for log in self.logs:
            if component is not None and log.get("component") != component:
                continue
            if level is not None and log.get("level") != level:
                continue
            if message_prefix is not None and not log.get("message", "").startswith(message_prefix):
                continue
            total += 1
        return total

    def component_log_counts(self):
        """Count log lines per component (activity heatmap), not actual calls."""
        counts = defaultdict(int)
        for log in self.logs:
            component = log.get("component")
            if component:
                counts[component] += 1
        return dict(counts)

    def workflow_count(self):
        """Number of distinct workflow runs (by trace id)."""
        traces = {
            log["trace_id"]
            for log in self.logs
            if log.get("trace_id") and log["trace_id"] != "-"
        }
        return len(traces)

    def error_count(self):
        return self._count(level="error")

    def llm_call_count(self):
        return self._count(component="llm")

    def mcp_call_count(self):
        return self._count(component="mcp", message_prefix="calling tool")

    def cache_hit_count(self):
        return self._count(component="cache", message_prefix="hit")

    def cache_miss_count(self):
        return self._count(component="cache", message_prefix="miss")

    def rag_query_count(self):
        return self._count(component="rag", message_prefix="retrieve()")

    # ── Analytics ───────────────────────────────────────────────────────
    def workflow_stats(self):
        """Summarize each workflow (by trace id): component counts, errors, duration."""
        workflows = {}
        for log in self.logs:
            trace_id = log.get("trace_id")
            if not trace_id or trace_id == "-":
                continue

            wf = workflows.setdefault(
                trace_id, {"components": defaultdict(int), "errors": 0}
            )
            component = log.get("component")
            if component:
                wf["components"][component] += 1
            if log.get("level") == "error":
                wf["errors"] += 1
            if component == "workflow" and log.get("duration_ms") is not None:
                wf["duration_ms"] = log["duration_ms"]
        return workflows

    def token_analytics(self):
        """Aggregate token usage and estimated cost across all LLM calls."""
        stats = defaultdict(int)
        for log in self.logs:
            if log.get("component") != "llm":
                continue
            stats["prompt_tokens"] += log.get("prompt_tokens") or 0
            stats["completion_tokens"] += log.get("completion_tokens") or 0
            stats["total_tokens"] += log.get("total_tokens") or 0

        calls = self._count(component="llm")
        stats["llm_calls"] = calls
        stats["avg_tokens_per_call"] = (
            round(stats["total_tokens"] / calls, 2) if calls else 0
        )

        stats["input_cost"] = round(
            stats["prompt_tokens"] / 1_000_000 * INPUT_COST_PER_1M, 6
        )
        stats["output_cost"] = round(
            stats["completion_tokens"] / 1_000_000 * OUTPUT_COST_PER_1M, 6
        )
        stats["workflow_cost"] = round(stats["input_cost"] + stats["output_cost"], 6)
        return stats
