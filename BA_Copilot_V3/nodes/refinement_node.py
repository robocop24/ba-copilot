from agents.refinement_agent import refinement_agent
from utils.prompt_loader import load_prompt


def _safe_json(value, fallback="N/A"):
    if value is not None and hasattr(value, "model_dump_json"):
        return value.model_dump_json(indent=2)
    return fallback


def refinement_node(state):
    prompt_template = load_prompt("refinement.txt")
    prompt = prompt_template.format(
        analysis=_safe_json(state.get("analysis")),
        stories=_safe_json(state.get("stories")),
        acceptance_criteria=_safe_json(state.get("acceptance_criteria")),
        estimation=_safe_json(state.get("estimation")),
        gaps=_safe_json(state.get("gaps")),
        review=_safe_json(state.get("review")),
    )

    refinement = refinement_agent(prompt=prompt)
    return {"refinement": refinement}