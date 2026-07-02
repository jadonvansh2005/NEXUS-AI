"""
Collaboration Strategy

Responsibilities

- Select collaboration strategy
- Determine execution flow
- Configure agent coordination

Future

- AI-generated Strategies
- Adaptive Collaboration
- Cost-aware Strategies
- Performance Optimization
"""

from __future__ import annotations

from agents.collaboration.collaboration_models import (
    CollaborationMode,
)

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class CollaborationStrategy:

    """
    Determines how participating
    agents should collaborate.
    """

    # =====================================================
    # Select Strategy
    # =====================================================

    def select(

        self,

        state: CollaborationState,

    ) -> CollaborationMode:

        #
        # Future:
        # Workflow Engine / Planner
        # will provide preferred strategy.
        #

        strategy = state.metadata.get(

            "collaboration_mode"

        )

        if isinstance(

            strategy,

            CollaborationMode,

        ):

            state.collaboration_mode = strategy

            return strategy

        #
        # Automatic Strategy Selection
        #

        total_agents = len(

            state.participating_agents

        )

        #
        # Single Agent
        #

        if total_agents <= 1:

            state.collaboration_mode = (

                CollaborationMode.SINGLE_AGENT

            )

        #
        # Parallel
        #

        elif self.can_run_parallel(

            state

        ):

            state.collaboration_mode = (

                CollaborationMode.PARALLEL

            )

        #
        # Default Pipeline
        #

        else:

            state.collaboration_mode = (

                CollaborationMode.PIPELINE

            )

        return state.collaboration_mode

    # =====================================================
    # Parallel?
    # =====================================================

    def can_run_parallel(

        self,

        state: CollaborationState,

    ) -> bool:

        #
        # Future:
        # Dependency Graph
        #

        return len(

            state.tasks

        ) > 1

    # =====================================================
    # Sequential?
    # =====================================================

    def is_pipeline(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.PIPELINE

        )

    # =====================================================
    # Parallel?
    # =====================================================

    def is_parallel(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.PARALLEL

        )

    # =====================================================
    # Single Agent?
    # =====================================================

    def is_single_agent(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.SINGLE_AGENT

        )

    # =====================================================
    # Hierarchical?
    # =====================================================

    def is_hierarchical(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.HIERARCHICAL

        )

    # =====================================================
    # Consensus?
    # =====================================================

    def is_consensus(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.CONSENSUS

        )

    # =====================================================
    # Voting?
    # =====================================================

    def is_voting(

        self,

        state: CollaborationState,

    ) -> bool:

        return (

            state.collaboration_mode

            == CollaborationMode.VOTING

        )