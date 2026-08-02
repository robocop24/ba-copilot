"""MCP Client — Connects to BA-MCP-Server and exercises all tools,
resources, and prompts.

Usage:
    python tests/test_client.py
"""

import asyncio

from fastmcp import Client


async def main():
    client = Client("BA_MCP_Server/server.py")

    async with client:
        # =================================================================
        # 1. TOOLS
        # =================================================================
        tools = await client.list_tools()

        print("=" * 60)
        print("AVAILABLE TOOLS")
        print("=" * 60)
        for tool in tools:
            print(f"  • {tool.name}")
            if tool.description:
                print(f"    {tool.description}")

        # --- retrieve_similar_brd ---
        for query in ["Customer Portal", "login", "payment", "unknown-topic"]:
            result = await client.call_tool(
                "retrieve_similar_brd", {"requirement": query}
            )
            text = getattr(result.content[0], "text", str(result.content[0]))
            print(f"\n  retrieve_similar_brd({query!r}):")
            print(f"  {text[:200]}...")

        # --- calulate_story_points ---
        for complexity in ["low", "medium", "high", "very_high", "invalid"]:
            try:
                result = await client.call_tool(
                    "calulate_story_points", {"complexity": complexity}
                )
                text = getattr(result.content[0], "text", str(result.content[0]))
                print(f"  calulate_story_points({complexity!r}) → {text}")
            except Exception as e:
                print(f"  calulate_story_points({complexity!r}) → ERROR: {e}")

        # --- load_requirement ---
        print("\n  --- load_requirement ---")
        result = await client.call_tool(
            "load_requirement", {"file_name": "requirement.txt"}
        )
        text = getattr(result.content[0], "text", str(result.content[0]))
        print(f"  {text[:200]}...")

        # =================================================================
        # 2. RESOURCES
        # =================================================================
        print("\n" + "=" * 60)
        print("AVAILABLE RESOURCES")
        print("=" * 60)

        resource_uris = [
            "ba://story_standard",
            "ba://acceptance_standard",
            "ba://review_checklist",
        ]
        for uri in resource_uris:
            resource = await client.read_resource(uri)
            text = resource[0].text if hasattr(resource[0], "text") else str(resource[0])
            print(f"\n  [{uri}]")
            print(f"  {text[:300]}...")

        # =================================================================
        # 3. PROMPTS
        # =================================================================
        print("\n" + "=" * 60)
        print("AVAILABLE PROMPTS")
        print("=" * 60)

        prompts = await client.list_prompts()
        for prompt in prompts:
            print(f"  • {prompt.name}")
            if prompt.description:
                print(f"    {prompt.description}")

        # --- analyze_requirement ---
        print("\n  --- analyze_requirement ---")
        prompt = await client.get_prompt(
            "analyze_requirement",
            {"requirement": "A customer wants to reset their password via email link"},
        )
        for msg in prompt.messages:
            print(f"  [{msg.role}]")
            print(f"  {msg.content.text[:300]}...")

        # --- generate_user_story ---
        print("\n  --- generate_user_story ---")
        prompt = await client.get_prompt(
            "generate_user_story",
            {"requirement": "Online banking customer wants to view last 12 months of transactions"},
        )
        for msg in prompt.messages:
            print(f"  [{msg.role}]")
            print(f"  {msg.content.text[:300]}...")

        # --- review_requirement ---
        print("\n  --- review_requirement ---")
        prompt = await client.get_prompt(
            "review_requirement",
            {
                "requirement": "As a user, I want to export my data to CSV.",
                "analysis": "Data export is needed for compliance (GDPR Article 20). "
                            "The user has access to order history, profile data, and payment receipts.",
            },
        )
        for msg in prompt.messages:
            print(f"  [{msg.role}]")
            print(f"  {msg.content.text[:300]}...")

        print("\n" + "=" * 60)
        print("All server features exercised successfully.")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())