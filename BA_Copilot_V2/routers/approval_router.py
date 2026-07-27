def approval_router(state):
    
    approved = state.get("approved", False)
    
    if approved:
        return "end"
    
    if state.get("iteration", 0) >= state.get("max_iterations", 3):
        print("⚠️ Max refinement iterations reached. Ending workflow.")
        return "end"
    
    return "refine"