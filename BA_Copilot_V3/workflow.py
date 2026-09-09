"""Reusable BA workflow runner.

Called by the CLI (`main.py`) and, in future, a FastAPI endpoint. All business
logic lives here so the caller only supplies a requirement and an approval hook.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from graph.graph import graph
from langgraph.types import Command
from llm.settings import MODEL_NAME
from prompts.prompt_versions import PROMPT_VERSIONS

from observability.logger import log_event
from observability.trace import generate_trace_id, set_trace_id

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def _serialize_state(state_values: dict) -> dict:
    """Convert pydantic models in state to plain dicts for JSON serialization."""
    serialized = {}
    for key, value in state_values.items():
        if hasattr(value, "model_dump"):
            serialized[key] = value.model_dump()
        else:
            serialized[key] = value
    return serialized


def _default_approve(message: str) -> bool:
    """CLI approval — prompt the human on stdin."""
    answer = input(f"{message} (y/n): ")
    return answer.lower() == "y"


def _save_report(final_state_values: dict) -> str:
    """Persist the final state as a JSON report; return its path."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = str(OUTPUT_DIR / f"ba_report_{timestamp}.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(_serialize_state(final_state_values), f, indent=2, ensure_ascii=False)
    return report_path


def run_ba_workflow(
    requirement_text: str,
    approve: Callable[[str], bool] | None = None,
    max_iterations: int = 3,
    max_approvals: int = 5,
) -> dict:
    """Run the BA pipeline end-to-end and persist the report.

    Args:
        requirement_text: the raw requirement text (already extracted by the
            caller from a file or an API request body).
        approve: human-in-the-loop hook — receives the approval message and
            returns True/False. Defaults to prompting on stdin (CLI). A FastAPI
            caller can pass its own (e.g. auto-approve or a stored decision).
        max_iterations: refinement loop cap, stored in the graph state.
        max_approvals: cap on how many approval interrupts to process.

    Returns:
        {"trace_id": str, "report_path": str, "final_state": dict}
    """
    approve = approve or _default_approve

    trace_id = generate_trace_id()
    set_trace_id(trace_id)

    # Unique thread_id per run so LangGraph doesn't resume stale checkpoints.
    config = {"configurable": {"thread_id": trace_id}}

    initial_state = {
        "requirement": requirement_text,
        "model_version": MODEL_NAME,
        "prompt_versions": PROMPT_VERSIONS,
        "iteration": 0,
        "max_iterations": max_iterations,
    }
    log_event("workflow", "prompt version", prompt_versions=PROMPT_VERSIONS)
    log_event("workflow", "model version", model_version=MODEL_NAME)

    print("Starting workflow...")
    start = time.perf_counter()
    for event in graph.stream(initial_state, config=config):
        node_name = next(iter(event.keys())) if event else "?"
        print(f"[NODE] {node_name}")

    # Human-in-the-loop: approval can fire repeatedly (refinement → planner).
    approval_count = 0
    snapshot = graph.get_state(config)
    while snapshot.next and approval_count < max_approvals:
        approved = approve("Approve the BA report?")
        print(f"User approval: {approved}")
        graph.invoke(Command(resume=approved), config=config)
        snapshot = graph.get_state(config)
        approval_count += 1

    final_state = graph.get_state(config)

    log_event(
        "workflow",
        "completed",
        duration_ms=round((time.perf_counter() - start) * 1000, 2),
    )

    report_path = _save_report(final_state.values)
    print(f"\nReport saved to: {report_path}")

    try:
        graph.get_graph().draw_mermaid_png(
            output_file_path=str(OUTPUT_DIR / "ba_copilot_graph.png")
        )
        print("Graph saved to: output/ba_copilot_graph.png")
    except (requests.exceptions.RequestException, ValueError):
        print("⚠️ Could not render graph PNG (network issue — mermaid.ink unreachable)")

    return {
        "trace_id": trace_id,
        "report_path": report_path,
        "final_state": _serialize_state(final_state.values),
    }
