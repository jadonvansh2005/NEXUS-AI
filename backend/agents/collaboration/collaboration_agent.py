"""
Collaboration Agent

Responsibilities

- Orchestrate multi-agent collaboration
- Delegate collaboration workflow
- Store collaboration results

Future

- Distributed Collaboration
- Swarm Intelligence
- Remote Agent Support
- Cross-Cluster Collaboration
"""

from __future__ import annotations

from agents.core.base_agent import (
    BaseAgent,
)

from agents.core.agent_state import (
    AgentState,
)

from agents.collaboration.agent_registry import (
    AgentRegistry,
)

from agents.collaboration.collaboration_manager import (
    CollaborationManager,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class CollaborationAgent(

    BaseAgent

):

    """
    Multi-Agent Collaboration Agent.
    """

    def __init__(

        self,

        registry: AgentRegistry,

    ):

        super().__init__(

            "CollaborationAgent"

        )

        self.registry = registry

        self.manager = (

            CollaborationManager(

                registry

            )

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: AgentState,

    ) -> AgentState:

        self.log(

            "Starting Multi-Agent Collaboration"

        )

        #
        # Build Collaboration State
        #

        collaboration_state = (

            CollaborationState(

                workflow_id=state.metadata.get(

                    "workflow_id",

                    "",

                ),

                tasks=state.metadata.get(

                    "workflow_tasks",

                    [],

                ),

                metadata={

                    "required_agents":

                        state.metadata.get(

                            "required_agents",

                            [],

                        ),

                    "default_agent":

                        state.metadata.get(

                            "default_agent",

                            "general",

                        ),

                    "collaboration_mode":

                        state.metadata.get(

                            "collaboration_mode",

                            None,

                        ),

                },

            )

        )

        #
        # Execute Collaboration
        #

        collaboration_state = (

            self.manager.execute(

                collaboration_state

            )

        )

        #
        # Store Results
        #

        state.metadata[

            "collaboration_mode"

        ] = (

            collaboration_state.collaboration_mode.value

        )

        state.metadata[

            "participating_agents"

        ] = (

            collaboration_state.participating_agents

        )

        state.metadata[

            "completed_agents"

        ] = (

            collaboration_state.completed_agents

        )

        state.metadata[

            "failed_agents"

        ] = (

            collaboration_state.failed_agents

        )

        state.metadata[

            "agent_results"

        ] = (

            collaboration_state.agent_results

        )

        state.metadata[

            "collaboration_result"

        ] = (

            collaboration_state.merged_result

        )

        state.collaboration_result = (

            collaboration_state

        )

        return state