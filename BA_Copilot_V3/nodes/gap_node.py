import time

from agents.gap_agent import gap_agent
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def gap_node(state):
    
    log_event("GAP", "Started")
    prompt_template = load_prompt("gap.txt")
    prompt = prompt_template.format(
        requirement=state["requirement"],
        analysis=state["analysis"].model_dump_json(indent=2),
    )

    start = time.perf_counter()
    gaps = gap_agent(prompt=prompt)
    log_event("GAP", "Completed",
              duration_ms=round((time.perf_counter() - start) * 1000, 2))

    return {
        "gaps": gaps
    }