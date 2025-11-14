"""A simple agent that uses a single tool to get the weather."""

import asyncio

from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from movie_catalog_agent_langgraph.agents.prompts import instruction_prompt
from movie_catalog_agent_langgraph.agents.tools import mcp_client


async def build_agent() -> CompiledStateGraph:
    """Create a simple agent that uses a single tool to get the weather."""
    return create_agent(
        # model="openai:gpt-4o-mini",
        model="anthropic:claude-sonnet-4-5-20250929",
        tools=await mcp_client.get_tools(),
        system_prompt=instruction_prompt,
    )


graph = asyncio.run(build_agent())
