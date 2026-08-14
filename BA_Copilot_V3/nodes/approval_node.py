from langgraph.types import interrupt

from observability.logger import log_event


def approval_node(state):
    
    log_event("APPROVAL", "Started")
    approval = interrupt(
        {
            "message":"Approve the BA artifacts"
        }
    )
    
    return {
        "approved":approval
    }