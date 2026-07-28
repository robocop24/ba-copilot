from langgraph.types import interrupt

def approval_node(state):
    
    approval = interrupt(
        {
            "message":"Approve the BA artifacts"
        }
    )
    
    return {
        "approved":approval
    }