from agents.acceptance_agent import acceptance_agent
from mcp_client.resource_cache import get_resource
from utils.prompt_loader import load_prompt


def acceptance_node(state):
    acceptance_standard = get_resource("ba://acceptance_standard")

    prompt_template = load_prompt("acceptance_criteria.txt")
    prompt = prompt_template.format(
        acceptance_standard=acceptance_standard,
        stories=state["stories"].model_dump_json(indent=2),
    )

    criteria = acceptance_agent(prompt=prompt)
    return {"acceptance_criteria": criteria}