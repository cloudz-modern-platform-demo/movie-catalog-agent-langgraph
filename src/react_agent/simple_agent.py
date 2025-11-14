"""A simple agent that uses a single tool to get the weather."""

import asyncio

from langchain.agents import create_agent

from react_agent.tools import mcp_client


async def create_simple_agent():
    """Create a simple agent that uses a single tool to get the weather."""
    agent = create_agent(
        # model="openai:gpt-4o-mini",
        model="anthropic:claude-sonnet-4-5-20250929",
        tools=await mcp_client.get_tools(),
        system_prompt="You are a helpful assistant",
    )
    return agent


graph = asyncio.run(create_simple_agent())
