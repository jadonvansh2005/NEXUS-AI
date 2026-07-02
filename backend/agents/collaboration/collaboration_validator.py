"""
Collaboration Validator

Responsibilities

- Validate collaboration state
- Validate participating agents
- Validate task assignments
- Validate collaboration workflow

Future

- Agent Health Checks
- Capability Validation
- Circular Dependency Detection
- Distributed Agent Validation
"""

from __future__ import annotations

from agents.collaboration.agent_registry import (
    AgentRegistry,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class CollaborationValidator:

    """
    Validate collaboration workflow before execution.
    """

    def __init__(

        self,

        registry: AgentRegistry,

    ):

        self.registry = registry

    # =====================================================
    # Public API
    # =====================================================

    def validate(

        self,

        state: CollaborationState,

    ) -> bool:

        if not self._validate_agents(

            state

        ):

            return False

        if not self._validate_tasks(

            state

        ):

            return False

        if not self._validate_assignments(

            state

        ):

            return False

        return True

    # =====================================================
    # Validate Agents
    # =====================================================

    def _validate_agents(

        self,

        state: CollaborationState,

    ) -> bool:

        if not state.participating_agents:

            return False

        for agent in state.participating_agents:

            if not self.registry.exists(

                agent

            ):

                return False

        return True

    # =====================================================
    # Validate Tasks
    # =====================================================

    def _validate_tasks(

        self,

        state: CollaborationState,

    ) -> bool:

        return len(

            state.tasks

        ) > 0

    # =====================================================
    # Validate Assignments
    # =====================================================

    def _validate_assignments(

        self,

        state: CollaborationState,

    ) -> bool:

        for task in state.tasks:

            if not task.assigned_agent:

                return False

            if not self.registry.exists(

                task.assigned_agent

            ):

                return False

        return True

    # =====================================================
    # Has Failed Agents
    # =====================================================

    def has_failures(

        self,

        state: CollaborationState,

    ) -> bool:

        return len(

            state.failed_agents

        ) > 0

    # =====================================================
    # Collaboration Completed
    # =====================================================

    def collaboration_completed(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            len(

                state.completed_agents

            )

            ==

            len(

                state.participating_agents

            )

        )