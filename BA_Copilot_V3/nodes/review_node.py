from agents.review_agent import review_agent
from utils.prompt_loader import load_prompt

def review_node(state):
    
    prompt_template = load_prompt("review.txt")
    prompt = prompt_template.format(
            analysis=state["analysis"].model_dump_json(indent=2),
            stories=state["stories"].model_dump_json(indent=2),
            gaps=state["gaps"].model_dump_json(indent=2),
        )
    
    review = review_agent(prompt=prompt)
    
    return {
            "review": review
        }