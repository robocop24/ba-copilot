"""
MCP Server — Business Analyst Assistant.

Provides tools, resources, and prompts to support business analysis workflows:
- Simple math tools (add, multiply)
- BRD knowledge retrieval
- BA standards and checklists (as resources)
- Prompt templates for generating user stories and reviewing requirements

Requires: pip install fastmcp
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastmcp import FastMCP
from prompts import registor_prompts
from resources import registor_resources
from tools import registor_tools

mcp = FastMCP("BA-MCP-Server")

registor_tools(mcp)
registor_resources(mcp)
registor_prompts(mcp)

if __name__ == "__main__":
    mcp.run()