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
import logging
import threading

from fastmcp import Client

from mcp_client import get_server_target

_CACHE: dict[str, str] = {}
_LOCK = threading.Lock()
logger = logging.getLogger(__name__)

def get_resource(uri: str) -> str:
    """
    Fetch an MCP resource by URI. Cached in memory after first call.

    Example URIs:
        "ba://story_standard"
        "ba://acceptance_standard"
        "ba://review_checklist"
    """
    if uri in _CACHE:
        logger.debug(f"CACHE HIT (after lock)-> {uri}")
        return _CACHE[uri]
        
    with _LOCK:
        # double-check uner lock
        if uri in _CACHE:
            logger.debug(f"CACHE HIT (after lock)-> {uri}")
            return _CACHE[uri]
        
        logger.info(f"[MCP] CACHE MISS -> {uri}")
        
        async def _fetch():
            client = Client(get_server_target())
            async with client:
                result = await client.read_resource(uri)
                return result[0].text
            
        try:
            content = asyncio.run(_fetch())
        except Exception:
            logger.exception(f"[MCP] Failed to fetch resource: {uri}")
            raise
        
        _CACHE[uri] = content
        logger.info("[MCP] CACHED -> %s (%d chars)", uri, len(content))
        return content
    