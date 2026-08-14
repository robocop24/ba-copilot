import time

from agents.story_agent import story_agent
from mcp_client.resource_cache import get_resource
from utils.prompt_loader import load_prompt

from observability.logger import log_event


def story_node(state):
    
    log_event("STORY", "Started")
    story_standard = get_resource("ba://story_standard")
    
    prompt_template = load_prompt("story.txt")
    prompt = prompt_template.format(
            analysis=state["analysis"].model_dump_json(indent=2),
            story_standard=story_standard,
        )
    
    start = time.perf_counter()
    stories = story_agent(prompt=prompt)
    log_event("STORY", "Completed",
              duration_ms=round((time.perf_counter() - start) * 1000, 2))
    
    return {
            "stories": stories
        }