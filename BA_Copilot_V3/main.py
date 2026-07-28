from graph.graph import graph
from document.document_processor import DocumentProcessor
from langgraph.types import Command

def main():
    
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
        print(f"\nEvent: {event}")
    
    # Check if workflow was interrupted
    snapshot = graph.get_state(config)
    if snapshot.next:
        approval = input("Approval BA Report? (y/n): ")
        print(f"User approval: {approval}")
        graph.invoke(
            Command(
                resume=approval.lower()=="y"
            ),
            config=config
        )
        
    
    print("\nRESULT")
    print("="*50)
    final_state = graph.get_state(config)
    print(final_state.values)
    
    graph.get_graph().draw_mermaid_png(output_file_path="ba_copilot_graph.png")

if __name__ == "__main__":
    main()