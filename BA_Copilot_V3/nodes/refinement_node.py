from agents.refinement_agent import refinement_agent
from utils.prompt_loader import load_prompt

def refinement_node(state):
    
    prompt_template = load_prompt("refinement.txt")
    prompt = prompt_template.format(
        analysis=state["analysis"].model_dump_json(indent=2),
        stories=state["stories"].model_dump_json(indent=2),
        gaps=state["gaps"].model_dump_json(indent=2),
        review=state["review"].model_dump_json(indent=2),
        )
    
    refinement = refinement_agent(prompt=prompt)
    
    return {
            "refinement": refinement
        }