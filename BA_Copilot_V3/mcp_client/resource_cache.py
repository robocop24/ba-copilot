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
import threading

from fastmcp import Client

from mcp_client import get_server_target
from observability.logger import log_event

_CACHE: dict[str, str] = {}
_LOCK = threading.Lock()

def get_resource(uri: str) -> str:
    """
    Fetch an MCP resource by URI. Cached in memory after first call.

    Example URIs:
        "ba://story_standard"
        "ba://acceptance_standard"
        "ba://review_checklist"
    """
    if uri in _CACHE:
        log_event("cache", f"hit {uri}")
        return _CACHE[uri]
        
    with _LOCK:
        # double-check uner lock
        if uri in _CACHE:
            log_event("cache", f"hit {uri}")
            return _CACHE[uri]
        
        log_event("cache", f"miss {uri}")
        
        async def _fetch():
            client = Client(get_server_target())
            async with client:
                result = await client.read_resource(uri)
                return result[0].text
            
        try:
            content = asyncio.run(_fetch())
        except Exception as e:
            log_event("cache", f"failed to fetch {uri}: {e}")
            raise
        
        _CACHE[uri] = content
        log_event("cache", f"cached {uri} ({len(content)} chars)")
        return content
    