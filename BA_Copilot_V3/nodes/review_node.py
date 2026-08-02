from agents.review_agent import review_agent
from utils.prompt_loader import load_prompt


def _safe_json(value, fallback="N/A"):
    """Return model_dump_json or fallback if value is None/missing."""
    if value is not None and hasattr(value, "model_dump_json"):
        return value.model_dump_json(indent=2)
    return fallback


def review_node(state):

    prompt_template = load_prompt("review.txt")
    prompt = prompt_template.format(
        analysis=_safe_json(state.get("analysis")),
        stories=_safe_json(state.get("stories")),
        gaps=_safe_json(state.get("gaps")),
        estimation=_safe_json(state.get("estimation")),
    )

    review = review_agent(prompt=prompt)

    return {
        "review": review
    }