from agents.story_agent import story_agent
from utils.prompt_loader import load_prompt

def story_node(state):
    
    prompt_template = load_prompt("story.txt")
    prompt = prompt_template.format(
            analysis=state["analysis"].model_dump_json(indent=2),
        )
    
    stories = story_agent(prompt=prompt)
    
    return {
            "stories": stories
        }