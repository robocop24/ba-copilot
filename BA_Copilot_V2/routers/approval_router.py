from langgraph.graph import END

def approval_router(state):
    
    approved = state["approved"]
    
    if approved:
        return "refinement_output"
    
    return END