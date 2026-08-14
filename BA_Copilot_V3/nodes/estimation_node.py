from agents.estimation_agent import estimation_agent
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def estimation_node(state):
    
    log_event("ESTIMATION", "Started")
    prompt_template = load_prompt("estimate_stories.txt")
    prompt = prompt_template.format(
        stories = state["stories"].model_dump_json(indent=2)
        )
    
    estimation = estimation_agent(prompt=prompt)
    
    return {
        "estimation":estimation
    }