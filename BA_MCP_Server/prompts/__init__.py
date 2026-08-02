from .analyze_requirement import analyze_requirement
from .generate_user_stories import generate_user_story
from .review_requirement import review_requirement


def registor_prompts(mcp):
    
    mcp.prompt()(analyze_requirement)
    mcp.prompt()(generate_user_story)
    mcp.prompt()(review_requirement)