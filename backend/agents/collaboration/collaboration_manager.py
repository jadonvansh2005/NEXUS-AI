"""
Collaboration Manager

Responsibilities

- Coordinate multi-agent collaboration
- Select participating agents
- Allocate tasks
- Execute collaboration strategy
- Merge responses

Future

- Distributed Agents
- Swarm Intelligence
- Consensus Learning
- Adaptive Collaboration
"""

from __future__ import annotations

# from typing import Any
# from typing import Dict

from agents.collaboration.agent_registry import (
    AgentRegistry,
)

from agents.collaboration.agent_selector import (
    AgentSelector,
)

from agents.collaboration.collaboration_logger import (
    CollaborationLogger,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)

from agents.collaboration.collaboration_strategy import (
    CollaborationStrategy,
)

from agents.collaboration.collaboration_validator import (
    CollaborationValidator,
)

from agents.collaboration.communication_bus import (
    CommunicationBus,
)

from agents.collaboration.response_merger import (
    ResponseMerger,
)

from agents.collaboration.task_allocator import (
    TaskAllocator,
)


class CollaborationManager:

    """
    Coordinates the complete
    Multi-Agent Collaboration pipeline.
    """

    def __init__(

        self,

        registry: AgentRegistry,

    ):

        self.registry = registry

        self.selector = (

            AgentSelector(

                registry

            )

        )

        self.allocator = (

            TaskAllocator()

        )

        self.strategy = (

            CollaborationStrategy()

        )

        self.bus = (

            CommunicationBus()

        )

        self.merger = (

            ResponseMerger()

        )

        self.validator = (

            CollaborationValidator(

                registry

            )

        )

        self.logger = (

            CollaborationLogger()

        )

    # =====================================================
    # Execute Collaboration
    # =====================================================

    def execute(

        self,

        state: CollaborationState,

    ) -> CollaborationState:

        #
        # Select Agents
        #

        self.selector.select(

            state

        )

        #
        # Strategy
        #

        self.strategy.select(

            state

        )

        #
        # Validate
        #

        if not self.validator.validate(

            state

        ):

            self.logger.validation_failed()

            return state

        #
        # Start
        #

        self.logger.collaboration_started(

            state

        )

        #
        # Allocate Tasks
        #

        assignments = (

            self.allocator.allocate(

                state

            )

        )

        #
        # Execute
        #

        for agent_name, tasks in assignments.items():

            agent = self.registry.get(

                agent_name

            )

            if agent is None:

                continue

            for task in tasks:

                self.logger.agent_assigned(

                    agent_name,

                    task.task_id,

                )

                try:

                    #
                    # Future:
                    # CommunicationBus
                    # will dispatch
                    # messages/events.
                    #

                    #
                    # TODO:
                    # Replace direct task execution with
                    # AgentExecutionContext in future integration.
                    #

                    result = agent.execute(

                        task

                    )

                    state.complete_agent(

                        agent_name,

                        result,

                    )

                    self.logger.agent_completed(

                        agent_name

                    )

                except Exception as error:

                    state.fail_agent(

                        agent_name,

                        str(

                            error

                        ),

                    )

                    self.logger.agent_failed(

                        agent_name,

                        str(

                            error

                        ),

                    )

        #
        # Merge
        #

        self.logger.merge_started()

        self.merger.merge(

            state

        )

        self.logger.merge_completed()

        #
        # Finish
        #

        self.logger.collaboration_completed(

            state

        )

        return state