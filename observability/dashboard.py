import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from observability.log_analyzer import LogAnalyzer


def _section(title):
    """Print a section header."""
    print(f"\n{title}")
    print("-" * 30)


def main():
    analyzer = LogAnalyzer()

    print("\n=== BA COPILOT DASHBOARD ===\n")

    _section("Counters (derived from logs)")
    print(f"workflows:     {analyzer.workflow_count()}")
    print(f"llm_calls:     {analyzer.llm_call_count()}")
    print(f"mcp_calls:     {analyzer.mcp_call_count()}")
    print(f"cache_hits:    {analyzer.cache_hit_count()}")
    print(f"cache_misses:  {analyzer.cache_miss_count()}")
    print(f"rag_queries:   {analyzer.rag_query_count()}")
    print(f"errors:        {analyzer.error_count()}")

    _section("Component Latency")
    for component, stats in analyzer.component_latency_stats().items():
        print(f"{component}: count={stats['count']} avg={stats['avg_ms']}ms "
              f"min={stats['min_ms']}ms max={stats['max_ms']}ms")

    _section("Component Log Counts")
    for component, count in analyzer.component_log_counts().items():
        print(f"{component}: {count}")

    slowest = analyzer.slowest_component()
    if slowest:
        name, stats = slowest
        _section("Slowest Component")
        print(f"{name}: avg {stats['avg_ms']}ms")

    _section("Workflow Analytics")
    for trace_id, stats in analyzer.workflow_stats().items():
        print(f"{trace_id[:8]}: components={dict(stats['components'])} "
              f"errors={stats['errors']} duration={stats.get('duration_ms')}ms")

    _section("Token & Cost Analytics")
    tokens = analyzer.token_analytics()
    print(f"llm_calls:           {tokens['llm_calls']}")
    print(f"prompt_tokens:       {tokens['prompt_tokens']}")
    print(f"completion_tokens:   {tokens['completion_tokens']}")
    print(f"total_tokens:        {tokens['total_tokens']}")
    print(f"avg_tokens_per_call: {tokens['avg_tokens_per_call']}")
    print(f"input_cost:          ${tokens['input_cost']}")
    print(f"output_cost:         ${tokens['output_cost']}")
    print(f"workflow_cost:       ${tokens['workflow_cost']}")


if __name__ == "__main__":
    main()
