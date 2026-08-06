def approval_router(state):

    if state.get("approved") is True:
        return "end"

    if state.get("iteration", 0) >= state.get("max_iterations", 3):
        print("⚠️ Max refinement iterations reached. Ending workflow.")
        return "end"

    return "refinement"