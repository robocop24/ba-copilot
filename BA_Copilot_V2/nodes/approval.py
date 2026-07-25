from langgraph.types import interrupt

def approval_node(state):
    print("<<<< Approval node reached")
    approval = interrupt({
        "message":"Approval BA Report?"
    })
    
    return { "approved":approval }