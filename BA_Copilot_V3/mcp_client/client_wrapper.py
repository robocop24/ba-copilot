"""
MCP client wrapper for tool calls.

Uses a module-level singleton Client to avoid spawning a new
stdio subprocess for every tool invocation. The subprocess is
created once on first use and reused across all subsequent calls.
"""

import asyncio

from fastmcp import Client

from mcp_client import get_server_target

_client: Client | None = None
_lock = asyncio.Lock()


async def _get_client() -> Client:
    """Return a long-lived Client singleton. Creates it on first call."""
    global _client
    if _client is not None:
        return _client
    async with _lock:
        if _client is not None:  # double-check under lock
            return _client
        _client = Client(get_server_target())
        await _client.__aenter__()
        return _client


class BAMCPClient:
    """Wrapper that reuses a single MCP subprocess across all tool calls."""

    async def _call_tool(self, tool_name: str, arguments: dict) -> str:
        client = await _get_client()
        result = await client.call_tool(tool_name, arguments)
        return result.content[0].text

    async def retrieve_similar_brd(self, requirement: str) -> str:
        return await self._call_tool(
            "retrieve_similar_brd",
            {"requirement": requirement},
        )

    async def calulate_story_points(self, complexity: str) -> int:
        return await self._call_tool(
            "calulate_story_points",
            {"complexity": complexity},
        )