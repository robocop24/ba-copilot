"""
Module-level cache for MCP resources.

Resources (story standards, review checklists, etc.) are static
BA knowledge that rarely changes. This module fetches them once
on first access and reuses the cached value — avoiding repeated
stdio subprocess spawns.

Usage from any node:
    from mcp_client.resource_cache import get_resource
    standard = get_resource("ba://story_standard")
"""

import asyncio

from fastmcp import Client

from mcp_client import get_server_target

_CACHE: dict[str, str] = {}


def get_resource(uri: str) -> str:
    """
    Fetch an MCP resource by URI. Cached in memory after first call.

    Example URIs:
        "ba://story_standard"
        "ba://acceptance_standard"
        "ba://review_checklist"
    """
    if uri in _CACHE:
        return _CACHE[uri]

    async def _fetch():
        client = Client(get_server_target())
        async with client:
            result = await client.read_resource(uri)
            return result.content[0].text

    content = asyncio.run(_fetch())
    _CACHE[uri] = content
    return content