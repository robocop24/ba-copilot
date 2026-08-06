from agents.planner_agent import planner_agent
from utils.prompt_loader import load_prompt


def _safe_context(value, fallback="No prior context available."):
    """Return model dump JSON or fallback if value is None."""
    if value is not None and hasattr(value, "model_dump_json"):
        return value.model_dump_json(indent=2)
    return fallback


def planner_node(state):
    prompt_template = load_prompt("planner.txt")
    prompt = prompt_template.format(
        requirement=state["requirement"],
        iteration=state.get("iteration", 0),
        max_iterations=state.get("max_iterations", 3),
        review_context=_safe_context(state.get("review")),
        refinement_context=_safe_context(state.get("refinement")),
    )

    plan = planner_agent(prompt)
    return {"plan": plan}