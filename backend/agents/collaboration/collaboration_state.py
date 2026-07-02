"""
Collaboration State

Responsibilities

- Runtime collaboration state
- Participating agents
- Task assignments
- Agent results
- Collaboration metadata

Future

- Distributed Agents
- Swarm Intelligence
- Agent Reputation
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field

from agents.collaboration.collaboration_models import (
    CollaborationMode,
    CollaborationStatus,
    CollaborationTask,
)


class CollaborationState(BaseModel):
    """
    Runtime state for Multi-Agent Collaboration.
    """

    # =====================================================
    # Workflow
    # =====================================================

    workflow_id: str = ""

    collaboration_mode: CollaborationMode = (
        CollaborationMode.SINGLE_AGENT
    )

    status: CollaborationStatus = (
        CollaborationStatus.PENDING
    )

    # =====================================================
    # Tasks
    # =====================================================

    tasks: List[CollaborationTask] = Field(
        default_factory=list
    )

    # =====================================================
    # Agents
    # =====================================================

    participating_agents: List[str] = Field(
        default_factory=list
    )

    completed_agents: List[str] = Field(
        default_factory=list
    )

    failed_agents: List[str] = Field(
        default_factory=list
    )

    # =====================================================
    # Results
    # =====================================================

    agent_results: Dict[str, Any] = Field(
        default_factory=dict
    )

    merged_result: Any = None

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    # =====================================================
    # Helpers
    # =====================================================

    def register_agent(

        self,

        agent_name: str,

    ) -> None:

        if agent_name not in self.participating_agents:

            self.participating_agents.append(
                agent_name
            )

    def complete_agent(

        self,

        agent_name: str,

        result: Any,

    ) -> None:

        self.agent_results[
            agent_name
        ] = result

        if agent_name not in self.completed_agents:

            self.completed_agents.append(
                agent_name
            )

    def fail_agent(

        self,

        agent_name: str,

        reason: Any = None,

    ) -> None:

        self.agent_results[
            agent_name
        ] = reason

        if agent_name not in self.failed_agents:

            self.failed_agents.append(
                agent_name
            )

    def set_merged_result(

        self,

        result: Any,

    ) -> None:

        self.merged_result = result

        self.status = (
            CollaborationStatus.COMPLETED
        )