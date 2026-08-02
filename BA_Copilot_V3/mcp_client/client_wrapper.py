import os

from fastmcp import Client

# Resolve the BA MCP Server directory (sibling to BA_Copilot_V3)
_MCP_SERVER_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "BA_MCP_Server")
)
_SERVER_PY = os.path.join(_MCP_SERVER_DIR, "server.py")


class BAMCPClient:
    """Wrapper around fastmcp.Client that connects to the BA MCP Server via stdio."""

    async def retrieve_similar_brd(self, requirement: str) -> str:
        # fastmcp auto-detects .py files and uses PythonStdioTransport
        client = Client(_SERVER_PY)

        async with client:
            result = await client.call_tool(
                "retrieve_similar_brd",
                {"requirement": requirement},
            )
            return result.content[0].text
        
    async def calulate_story_points(self, complexity:str)-> int:
        client = Client(_SERVER_PY)
        
        async with client:
            result = await client.call_tool(
                "calulate_story_points",
                { "complexity": complexity }
            )
            return result.content[0].text