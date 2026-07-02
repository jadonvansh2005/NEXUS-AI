"""
Task Allocator

Responsibilities

- Assign workflow tasks to agents
- Balance workload
- Prepare execution assignments

Future

- Load Balancing
- Agent Capability Scoring
- Dynamic Task Reallocation
- Cost-based Allocation
"""

from __future__ import annotations

from typing import Dict
from typing import List

from agents.collaboration.collaboration_models import (
    CollaborationTask,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class TaskAllocator:

    """
    Assign workflow tasks to
    participating agents.
    """

    # =====================================================
    # Allocate
    # =====================================================

    def allocate(

        self,

        state: CollaborationState,

    ) -> Dict[str, List[CollaborationTask]]:

        assignments: Dict[str, List[CollaborationTask]] = {}

        #
        # Allocate according to the
        # assigned agent.
        #

        for task in state.tasks:

            if not task.assigned_agent:

                continue

            assignments.setdefault(

                task.assigned_agent,

                []

            ).append(

                task

            )

        return assignments

    # =====================================================
    # Agent Tasks
    # =====================================================

    def tasks_for_agent(

        self,

        agent_name: str,

        state: CollaborationState,

    ) -> List[CollaborationTask]:

        return [

            task

            for task

            in state.tasks

            if task.assigned_agent == agent_name

        ]

    # =====================================================
    # Has Tasks
    # =====================================================

    def has_tasks(

        self,

        agent_name: str,

        state: CollaborationState,

    ) -> bool:

        return (

            len(

                self.tasks_for_agent(

                    agent_name,

                    state,

                )

            )

            > 0

        )

    # =====================================================
    # Task Count
    # =====================================================

    def task_count(

        self,

        state: CollaborationState,

    ) -> Dict[str, int]:

        counts: Dict[str, int] = {}

        for task in state.tasks:

            if not task.assigned_agent:

                continue

            counts[

                task.assigned_agent

            ] = (

                counts.get(

                    task.assigned_agent,

                    0,

                )

                + 1

            )

        return counts