from langchain_core.tools import tool
from mcp_client.client_wrapper import calulate_story_points as _calulate
from mcp_client.client_wrapper import retrieve_similar_brd as _retrieve


@tool
def retrieve_similar_brd(requirement: str) -> str:
    """
    Retrieve similar BRD context from BA MCP Server
    """
    return _retrieve(requirement)


@tool
def calulate_story_points(complexity: str) -> int:
    """Calculate story points based on complexity"""
    return _calulate(complexity)