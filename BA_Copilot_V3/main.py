import json
import logging
import os
from datetime import datetime, timezone

import requests
from document.document_processor import DocumentProcessor
from graph.graph import graph
from langgraph.types import Command


def _serialize_state(state_values: dict) -> dict:
    """Convert pydantic models in state to plain dicts for JSON serialization."""
    serialized = {}
    for key, value in state_values.items():
        if hasattr(value, "model_dump"):
            serialized[key] = value.model_dump()
        else:
            serialized[key] = value
    return serialized


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    # Silence noisy third-party loggers
    for lib in ("httpx", "httpcore", "openai", "langchain", "langgraph"):
        logging.getLogger(lib).setLevel(logging.WARNING)
    
    processor = DocumentProcessor()
    requirement = processor.extract_text("input/requirement.txt")
    config={
            "configurable":{
                "thread_id":"portal_project_v3"
            }
        }

    # Stream events to catch interrupts
    print("Starting workflow...")
    for event in graph.stream({
        "requirement": requirement,
        "iteration": 0,
        "max_iterations": 3
        }, config=config):
        node_name = next(iter(event.keys())) if event else "?"
        print(f"[NODE] {node_name}")

    # Loop to handle multiple interrupts (approval can fire repeatedly via refinement → planner)
    approval_count = 0
    max_approvals = 5
    snapshot = graph.get_state(config)
    while snapshot.next and approval_count < max_approvals:
        approval = input("Approval BA Report? (y/n): ")
        print(f"User approval: {approval}")
        graph.invoke(
            Command(resume=approval.lower() == "y"),
            config=config,
        )
        snapshot = graph.get_state(config)
        approval_count += 1
        
    
    # print("\nRESULT")
    # print("="*50)
    final_state = graph.get_state(config)
    # print(final_state.values)
    
    # Save report to output folder as JSON
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = f"output/ba_report_{timestamp}.json"
    
    serialized = _serialize_state(final_state.values)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved to: {report_path}")

    try:
        graph.get_graph().draw_mermaid_png(output_file_path="ba_copilot_graph.png")
        print("Graph saved to: ba_copilot_graph.png")
    except (requests.exceptions.RequestException, ValueError):
        print("⚠️ Could not render graph PNG (network issue — mermaid.ink unreachable)")

if __name__ == "__main__":
    main()