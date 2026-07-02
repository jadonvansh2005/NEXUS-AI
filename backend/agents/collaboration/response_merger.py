"""
Response Merger

Responsibilities

- Merge agent responses
- Resolve conflicts
- Produce final collaboration response

Future

- LLM-based Response Fusion
- Conflict Resolution
- Confidence Scoring
- Source Attribution
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from agents.collaboration.collaboration_state import (
    CollaborationState,
)


class ResponseMerger:

    """
    Merges outputs from multiple agents
    into one final response.
    """

    # =====================================================
    # Merge
    # =====================================================

    def merge(

        self,

        state: CollaborationState,

    ) -> Any:

        #
        # Future:
        # Use LLM to intelligently
        # merge responses.
        #

        merged = {

            "workflow_id": state.workflow_id,

            "agents": {},

            "summary": "",

        }

        for agent_name, result in (

            state.agent_results.items()

        ):

            merged["agents"][

                agent_name

            ] = result

        merged["summary"] = (

            self.build_summary(

                state

            )

        )

        state.set_merged_result(

            merged

        )

        return merged

    # =====================================================
    # Build Summary
    # =====================================================

    def build_summary(

        self,

        state: CollaborationState,

    ) -> str:

        completed = len(

            state.completed_agents

        )

        failed = len(

            state.failed_agents

        )

        return (

            f"{completed} agent(s) "

            f"completed successfully, "

            f"{failed} failed."

        )

    # =====================================================
    # Successful Results
    # =====================================================

    def successful_results(

        self,

        state: CollaborationState,

    ) -> Dict[str, Any]:

        return {

            agent: state.agent_results[

                agent

            ]

            for agent in state.completed_agents

            if agent in state.agent_results

        }

    # =====================================================
    # Failed Results
    # =====================================================

    def failed_results(

        self,

        state: CollaborationState,

    ) -> Dict[str, Any]:

        return {

            agent: state.agent_results[

                agent

            ]

            for agent in state.failed_agents

            if agent in state.agent_results

        }

    # =====================================================
    # Agent Count
    # =====================================================

    def total_agents(

        self,

        state: CollaborationState,

    ) -> int:

        return len(

            state.participating_agents

        )