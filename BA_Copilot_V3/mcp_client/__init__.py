"""
Shared MCP client configuration.

Both client_wrapper (tools) and resource_cache (resources) connect
to the same BA MCP Server. The server target is resolved once here.
"""

import os

_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "..", "BA_MCP_Server", "server.py"
)
_LOCAL = os.path.abspath(_SCRIPT)

# Set MCP_SERVER_URL to switch from local stdio to remote HTTP.
# Example: "https://ba-mcp.example.com/mcp"
_REMOTE = os.getenv("MCP_SERVER_URL", "")


def get_server_target() -> str:
    """
    Returns the MCP server target for fastmcp.Client.

    - If MCP_SERVER_URL is set, returns the HTTP URL.
    - Otherwise returns the absolute path to the local server.py (stdio).
    """
    return _REMOTE or _LOCAL
