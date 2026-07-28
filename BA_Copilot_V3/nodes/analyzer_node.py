from utils.prompt_loader import load_prompt
from agents.analyzer_agent import analyzer_agent

def analyzer_node(state):

    prompt_template = load_prompt("analyzer.txt")
    prompt = prompt_template.format(requirement=state['requirement'])

    analysis = analyzer_agent(prompt=prompt)

    return {
        "analysis": analysis
    }