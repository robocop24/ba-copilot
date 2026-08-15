from langchain_core.tools import tool
from mcp_client.client_wrapper import calculate_story_points as _calculate
from mcp_client.client_wrapper import retrieve_similar_brd as _retrieve

from observability.metrics_registry import metrics


@tool
def retrieve_similar_brd(requirement: str) -> str:
    """
    Retrieve similar BRD context from BA MCP Server
    """
    metrics.increment("tool_calls")
    return _retrieve(requirement)


@tool
def calculate_story_points(complexity: str) -> int:
    """Calculate story points based on complexity."""
    metrics.increment("tool_calls")
    return _calculate(complexity)