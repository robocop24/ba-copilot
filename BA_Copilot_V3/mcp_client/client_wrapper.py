"""
MCP client wrapper for tool calls.

Each call spawns a short-lived MCP subprocess via asyncio.run()
because LangGraph ToolNode invokes tools synchronously in a thread pool.
The per-call overhead is acceptable for BA workflows that make
only a handful of tool invocations per run.
"""

import asyncio
import logging

from fastmcp import Client

from mcp_client import get_server_target

logger = logging.getLogger(__name__)

async def _call_tool(tool_name: str, arguments: dict) -> str:
    """Connect, call a single tool, and disconnect."""
    client = Client(get_server_target())
    logger.info(f"[MCP] Calling Tool -> {tool_name}")
    async with client:
        result = await client.call_tool(tool_name, arguments)
        logger.info(f"[MCP] Tool Completed-> {tool_name}")
        return result.content[0].text


def retrieve_similar_brd(requirement: str) -> str:
    return asyncio.run(_call_tool(
        "retrieve_similar_brd",
        {"requirement": requirement},
    ))


def calculate_story_points(complexity: str) -> int:
    result = asyncio.run(_call_tool(
        "calculate_story_points",
        {"complexity": complexity},
    ))
    return int(result)