"""Main module."""

import asyncio
import logging
import sys

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv

from movie_catalog_agent_langgraph.executor.agent_executor import MovieCatalogAgentExecutor
from movie_catalog_agent_langgraph.agents.graph import graph as movie_catalog_agent
from movie_catalog_agent_langgraph.agents.tools import mcp_client

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

async def main(host: str, port: int):
    """Run the main function."""
    try:
        agent_executor = await MovieCatalogAgentExecutor.initialize(
            agent=movie_catalog_agent,
            tools=await mcp_client.get_tools(),
            stream_mode="messages",
            # stream_mode="values",
        )
        capabilities = AgentCapabilities(
            streaming=True if agent_executor.stream_mode == "messages" else False,
            pushNotifications=True,
        )

        skills = []

        for agent_tool in agent_executor.get_agent_tools():
            skills.append(
                AgentSkill(
                    id=agent_tool.name,
                    name=agent_tool.name,
                    description=agent_tool.description,
                    tags=[],
                    examples=[],
                )
            )
        agent_card = AgentCard(
            name="Movie Catalog Agent",
            description="Helps with movie catalog management",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            default_input_modes=SUPPORTED_CONTENT_TYPES,
            default_output_modes=SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=skills,
        )

        # --8<-- [start:DefaultRequestHandler]
        # httpx_client = httpx.AsyncClient(timeout=300)
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
            # push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        return server

    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        sys.exit(1)


def run():
    host = "0.0.0.0"
    port = 8300
    server = asyncio.run(main(host=host, port=port))
    uvicorn.run(server.build(), host=host, port=port)
