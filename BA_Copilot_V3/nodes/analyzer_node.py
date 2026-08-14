import time

from agents.analyzer_agent import analyzer_agent
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def analyzer_node(state):
    
    log_event("ANALYZER", "Started")
    prompt_template = load_prompt("analyzer.txt")
    prompt = prompt_template.format(requirement=state['requirement'])

    start = time.perf_counter()
    analysis = analyzer_agent(prompt=prompt)
    log_event("ANALYZER", "Completed",
              duration_ms=round((time.perf_counter() - start) * 1000, 2))

    return {
        "analysis": analysis
    }