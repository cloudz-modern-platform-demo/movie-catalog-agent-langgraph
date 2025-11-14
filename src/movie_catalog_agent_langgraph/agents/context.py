"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Any

from . import prompts


@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    system_prompt: str = field(
        default=prompts.instruction_prompt,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-sonnet-4-5-20250929",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    user_id: str = field(
        default="",
        metadata={
            "description": "The user id for the agent's interactions."
        },
    )
    thread_id: str = field(
        default="",
        metadata={
            "description": "The thread id for the agent's interactions."
        },
    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        for f in fields(self):
            if not f.init:
                continue

            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))

    def model_dump(self) -> dict[str, Any]:
        """Dump the configuration to a dictionary."""
        return {f.name: getattr(self, f.name) for f in fields(self) if f.init}
