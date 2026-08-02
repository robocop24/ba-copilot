import asyncio
import os
import sys

# Ensure BA_Copilot_V3 is on sys.path when running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client.client_wrapper import BAMCPClient


async def main():
    mcp = BAMCPClient()

    context = await mcp.retrieve_similar_brd("build customer portal")

    print(context)


if __name__ == "__main__":
    asyncio.run(main())