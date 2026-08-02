from .calculate_story_points import calulate_story_points
from .load_requirement import load_requirement
from .retrieve_similar_brd import retrieve_similar_brd


def registor_tools(mcp):
    
    mcp.add_tool(retrieve_similar_brd)
    mcp.add_tool(calulate_story_points)
    mcp.add_tool(load_requirement)