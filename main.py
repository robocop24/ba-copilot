import json
from workflow.orchestrator import WorkflowOchestrator
from document.document_processor import DocumentProcessor

def main():

    orchestrator = WorkflowOchestrator()
    processor = DocumentProcessor()

    file_path = "samples/requirement.txt"  # Replace with your file path
    try:
        requirement = processor.extract_text(file_path)
    except ValueError as e:
        print(e)

    state = orchestrator.run(requirement)

    print(json.dumps(state.to_dict(), indent=4))

    with open("outputs/ba_report.json", "w", encoding="utf-8") as file:
        json.dump(state.to_dict(), file, indent=4)

if __name__ == "__main__":
    main()