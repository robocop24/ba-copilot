"""
MCP client wrapper — persistent connection, thread-safe.

A single MCP server subprocess is started at import time and stays alive.
One dedicated asyncio event loop runs in a daemon thread.  LangGraph's
thread-pool-based ToolNode submits calls via run_coroutine_threadsafe(),
so parallel tool invocations share one server, one model, one cache.
"""
import asyncio
import atexit
import logging
import threading

from fastmcp import Client

from mcp_client import get_server_target

logger = logging.getLogger(__name__)

# ── Persistent event loop + client (module-level singleton) ──────────
_loop: asyncio.AbstractEventLoop
_client: Client
_ready = threading.Event()


def _run_event_loop() -> None:
    """Daemon thread target — starts the loop, connects, then waits forever."""
    global _loop, _client
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    async def _connect() -> None:
        global _client
        _client = Client(get_server_target())
        await _client.__aenter__()
        logger.info("[MCP] Persistent server connected")
        _ready.set()
        # Keep the loop alive indefinitely
        await asyncio.Event().wait()

    _loop.run_until_complete(_connect())


def _cleanup() -> None:
    """Disconnect the persistent client on interpreter shutdown."""
    if _client is not None and _loop is not None and not _loop.is_closed():
        try:
            future = asyncio.run_coroutine_threadsafe(
                _client.__aexit__(None, None, None), _loop
            )
            future.result(timeout=5)
        except Exception:
            pass


_thread = threading.Thread(target=_run_event_loop, daemon=True, name="mcp-loop")
_thread.start()
_ready.wait(timeout=30)  # block until connected (or timeout in CI)
atexit.register(_cleanup)


# ── Public API ───────────────────────────────────────────────────────
def _call_tool_sync(tool_name: str, arguments: dict) -> str:
    """Thread-safe: submit to the persistent loop and block for result."""
    async def _call() -> str:
        logger.info("[MCP] Calling Tool -> %s", tool_name)
        result = await _client.call_tool(tool_name, arguments)
        logger.info("[MCP] Tool Completed -> %s", tool_name)
        return result.content[0].text

    future = asyncio.run_coroutine_threadsafe(_call(), _loop)
    return future.result()


def retrieve_similar_brd(requirement: str) -> str:
    return _call_tool_sync("retrieve_similar_brd", {"requirement": requirement})


def calculate_story_points(complexity: str) -> int:
    return int(_call_tool_sync("calculate_story_points", {"complexity": complexity}))