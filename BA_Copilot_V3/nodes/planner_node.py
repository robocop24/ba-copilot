from agents.planner_agent import planner_agent
from utils.prompt_loader import load_prompt

def planner_node(state):
    
    prompt_template = load_prompt("planner.txt")
    prompt = prompt_template.format(requirement=state['requirement'])
    
    plan = planner_agent(prompt)
    
    return { "plan": plan }