from langgraph.types import interrupt

def approval_node(state):
    approval = interrupt({
        "message":"Approval BA Report?"
    })
    
    return { "approved":approval }