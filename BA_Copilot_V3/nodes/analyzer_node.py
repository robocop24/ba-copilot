from agents.analyzer_agent import analyzer_agent
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def analyzer_node(state):
    
    log_event("ANALYZER", "Started")
    prompt_template = load_prompt("analyzer.txt")
    prompt = prompt_template.format(requirement=state['requirement'])

    analysis = analyzer_agent(prompt=prompt)

    return {
        "analysis": analysis
    }