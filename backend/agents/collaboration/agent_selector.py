"""
Agent Selector

Responsibilities

- Select participating agents
- Detect multi-agent requirements
- Support single and multi-agent workflows

Future

- LLM-based Agent Selection
- Dynamic Agent Discovery
- Agent Capability Matching
- Confidence-based Selection
"""

from __future__ import annotations

from typing import List

from agents.collaboration.agent_registry import (
    AgentRegistry,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class AgentSelector:

    """
    Select agents required for a workflow.
    """

    def __init__(

        self,

        registry: AgentRegistry,

    ):

        self.registry = registry

    # =====================================================
    # Select Agents
    # =====================================================

    def select(

        self,

        state: CollaborationState,

    ) -> List[str]:

        #
        # Future:
        # Workflow Engine will provide
        # required agents.
        #

        requested_agents = (

            state.metadata.get(

                "required_agents",

                [],

            )

        )

        selected_agents: List[str] = []

        for agent_name in requested_agents:

            if self.registry.exists(

                agent_name

            ):

                selected_agents.append(

                    agent_name

                )

        #
        # Fallback
        #

        if not selected_agents:

            default_agent = (

                state.metadata.get(

                    "default_agent",

                    "general",

                )

            )

            if self.registry.exists(

                default_agent

            ):

                selected_agents.append(

                    default_agent

                )

        #
        # Register participating agents
        #

        for agent in selected_agents:

            state.register_agent(

                agent

            )

        return selected_agents

    # =====================================================
    # Single Agent?
    # =====================================================

    def is_single_agent(

        self,

        agents: List[str],

    ) -> bool:

        return len(

            agents

        ) == 1

    # =====================================================
    # Multi Agent?
    # =====================================================

    def is_multi_agent(

        self,

        agents: List[str],

    ) -> bool:

        return len(

            agents

        ) > 1