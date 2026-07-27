from graph import graph
from langgraph.types import Command
from document.document_processor import DocumentProcessor

def main():
    
    processor = DocumentProcessor()
    requirement = processor.extract_text("input/requirement.txt")
    config={
            "configurable":{
                "thread_id":"portal_project"
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
    state = graph.get_state(config)
    print(f"\nCurrent state after stream: {state}")
    
    # If interrupted, show the approval prompt and resume
    if state.next:
        print(f"\nInterrupt detected. Nodes pending: {state.next}")
        user_input = input("Approve BA Report? (yes/no): ").lower()
        approval = user_input == "yes"
        print(f"User approval: {approval}")
        
        # Resume with approval decision
        result = graph.invoke(Command(resume=approval), config=config)
        print(f"\nResumed workflow result: {result}")
    
    print("\nRESULT")
    print("="*50)
    final_state = graph.get_state(config)
    print(final_state.values)
    
    graph.get_graph().draw_mermaid_png(output_file_path="ba_copilot_graph.png")

if __name__ == "__main__":
    main()