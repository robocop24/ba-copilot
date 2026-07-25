import json
from workflow.orchestrator import WorkflowOchestrator
from document.document_processor import DocumentProcessor


def build_state(file_path: str = "samples/requirement.txt"):
    orchestrator = WorkflowOchestrator()
    processor = DocumentProcessor()

    requirement = processor.extract_text(file_path)
    state = orchestrator.run(requirement)

    with open("outputs/ba_report.json", "w", encoding="utf-8") as file:
        json.dump(state.to_dict(), file, indent=4)

    return state


def main():
    try:
        state = build_state()
    except ValueError as e:
        print(e)
        return

    print(json.dumps(state.to_dict(), indent=4))


if __name__ == "__main__":
    main()