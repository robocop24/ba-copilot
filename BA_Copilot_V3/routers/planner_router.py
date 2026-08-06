_VALID_STEPS = {"analyze_requirements", "done"}


def planner_router(state):
    step = state["plan"].next_step
    if step not in _VALID_STEPS:
        return "done"
    return step