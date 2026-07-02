"""
Memory State

Responsibilities

- Runtime memory state
- Retrieved memories
- Retrieved facts
- Knowledge context
- Memory metadata

Future

- Reflection Feedback
- Confidence Scores
- Source Attribution
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field

from agents.memory_agent.memory_models import (
    MemoryAction,
    MemoryType,
    RetrievalMode,
)


# ==========================================================
# Memory State
# ==========================================================

class MemoryState(BaseModel):
    """
    Runtime state of the Memory Agent.
    """

    #
    # User
    #

    user_id: int

    query: str

    #
    # Retrieval
    #

    retrieval_mode: RetrievalMode = (
        RetrievalMode.HYBRID
    )

    #
    # Memory Sources
    #

    requested_memory_types: List[MemoryType] = Field(

        default_factory=list

    )

    #
    # Retrieved Data
    #

    retrieved_facts: List[Any] = Field(

        default_factory=list

    )

    retrieved_episodes: List[Any] = Field(

        default_factory=list

    )

    retrieved_semantic: List[Any] = Field(

        default_factory=list

    )

    retrieved_knowledge: List[Any] = Field(

        default_factory=list

    )

    retrieved_short_term: List[Any] = Field(

        default_factory=list

    )

    retrieved_long_term: List[Any] = Field(

        default_factory=list

    )

    #
    # Final Context
    #

    context: List[Any] = Field(

        default_factory=list

    )

    #
    # Memory Writing
    #

    action: MemoryAction = (

        MemoryAction.READ

    )

    memory_to_store: Dict[str, Any] = Field(

        default_factory=dict

    )

    #
    # Metadata
    #

    metadata: Dict[str, Any] = Field(

        default_factory=dict

    )

    # =====================================================
    # Helpers
    # =====================================================

    def add_context(

        self,

        memory: Any,

    ) -> None:

        self.context.append(

            memory

        )

    def add_fact(

        self,

        fact: Any,

    ) -> None:

        self.retrieved_facts.append(

            fact

        )

    def add_episode(

        self,

        episode: Any,

    ) -> None:

        self.retrieved_episodes.append(

            episode

        )

    def add_semantic(

        self,

        memory: Any,

    ) -> None:

        self.retrieved_semantic.append(

            memory

        )

    def add_knowledge(

        self,

        memory: Any,

    ) -> None:

        self.retrieved_knowledge.append(

            memory

        )