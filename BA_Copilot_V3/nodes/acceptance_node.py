import time

from agents.acceptance_agent import acceptance_agent
from mcp_client.resource_cache import get_resource
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def acceptance_node(state):
    
    log_event("ACCEPTANCE", "Started")
    start = time.perf_counter()
    acceptance_standard = get_resource("ba://acceptance_standard")

    prompt_template = load_prompt("acceptance_criteria.txt")
    prompt = prompt_template.format(
        acceptance_standard=acceptance_standard,
        stories=state["stories"].model_dump_json(indent=2),
    )

    criteria = acceptance_agent(
        prompt=prompt,
        expected_stories=len(state["stories"].user_stories),
    )
    log_event("ACCEPTANCE", "Completed",
              duration_ms=round((time.perf_counter() - start) * 1000, 2))
    return {"acceptance_criteria": criteria}