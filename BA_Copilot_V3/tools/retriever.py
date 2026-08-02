import asyncio

from langchain_core.tools import tool
from mcp_client.client_wrapper import BAMCPClient


@tool
def retrieve_similar_brd(requirement:str)->str:
    """
    Retrieve similar BRD context from BA MCP Server
    """
    
    mcp_client = BAMCPClient()
    
    return asyncio.run(
        mcp_client.retrieve_similar_brd(requirement)
        )
    
@tool
def calulate_story_points(complexity:str)->int:
    """Calulate story points based on compexity"""
    mcp_client = BAMCPClient()
    
    return asyncio.run(
        mcp_client.calulate_story_points(complexity)
        )