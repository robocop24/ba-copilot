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
import time

from mcp_client.client_wrapper import _client, _loop, _ready
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

        # Reuse the persistent client from client_wrapper — avoids spawning a
        # fresh stdio subprocess (and its ~20s cold start) on every miss.
        _ready.wait(timeout=120)
        if not _ready.is_set():
            raise RuntimeError(
                f"MCP server not ready; cannot fetch resource {uri}"
            )

        async def _fetch():
            result = await _client.read_resource(uri)
            return result[0].text

        start = time.perf_counter()
        try:
            future = asyncio.run_coroutine_threadsafe(_fetch(), _loop)
            content = future.result()
        except Exception as e:
            log_event("cache", f"failed to fetch {uri}: {e}", level="error")
            raise

        _CACHE[uri] = content
        log_event("cache", f"cached {uri} ({len(content)} chars)",
                  duration_ms=round((time.perf_counter() - start) * 1000, 2))
        return content
    