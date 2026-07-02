"""
Tool Selector Agent

Responsibilities

- Receive PlannerTask
- Match required capabilities
- Find candidate tools
- Rank tools
- Select provider
- Return selected tool

Future

- LLM Tool Selection
- Semantic Search
- Reflection Feedback
- Dynamic Tool Discovery
"""

from __future__ import annotations

from typing import Optional

from agents.planner.schemas import (
    PlannerTask,
)

from agents.tool_selection.capability_matcher import (
    CapabilityMatcher,
)

from agents.tool_selection.tool_matcher import (
    ToolMatcher,
)

from agents.tool_selection.tool_ranker import (
    ToolRanker,
)

from agents.tool_selection.provider_selector import (
    ProviderSelector,
)

from agents.tool_selection.fallback_selector import (
    FallbackSelector,
)

from agents.tool_selection.tool_logger import (
    ToolLogger,
)

from agents.core.agent_state import (
    AgentState,
)

from agents.core.tool_registry import (
    ToolRegistry,
)

from agents.tool_selection.provider_registry import (
    ProviderRegistry,
)


class ToolSelectorAgent:

    """
    Main Tool Selection Engine.
    """

    def __init__(

        self,

        registry: ToolRegistry,

        provider_registry: ProviderRegistry,

    ):

        self.capability_matcher = (
            CapabilityMatcher()
        )

        self.registry = registry

        self.tool_matcher = (

            ToolMatcher(

                self.registry

            )

        )
        self.tool_ranker = (
            ToolRanker()
        )

        

        self.fallback_selector = (
            FallbackSelector()
        )

        self.logger = (
            ToolLogger()
        )

        self.provider_registry = (

            provider_registry

        )

        self.provider_selector = (

            ProviderSelector(

                self.provider_registry

            )

        )

    # =====================================================
    # Select Tool
    # =====================================================

    def select_tool(
        self,
        task: PlannerTask,
    ) -> Optional[dict]:

        #
        # -----------------------------------------
        # Capability Matching
        # -----------------------------------------
        #

        capabilities = (

            self.capability_matcher.match(
                task,
                self.registry
            )

        )

        self.logger.capability_detected(
            capabilities
        )

        #
        # -----------------------------------------
        # Candidate Tools
        # -----------------------------------------
        #

        candidates = (

            self.tool_matcher.match(
                capabilities
            )

        )

        self.logger.candidate_tools(
            candidates
        )

        #
        # -----------------------------------------
        # Ranking
        # -----------------------------------------
        #

        tool = (

            self.tool_ranker.rank(
                candidates
            )

        )

        if tool is None:

            self.logger.selection_failed(

                "No matching tool found."

            )

            return None

        self.logger.tool_selected(
            tool
        )

        #
        # -----------------------------------------
        # Provider Selection
        # -----------------------------------------
        #

        provider = (

            self.provider_selector.select(
                tool
            )

        )

        self.logger.provider_selected(
            provider
        )

        #
        # -----------------------------------------
        # Result
        # -----------------------------------------
        #

        return {

            "tool": tool,

            "provider": provider,

            "capabilities": capabilities,

        }
    

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: AgentState,

    ) -> AgentState:

        selected_tools = []

        execution_plan = state.execution_plan

        if not execution_plan:

            return state

        for task in execution_plan.tasks:

            result = self.select_tool(

                task

            )

            if result:

                selected_tools.append(

                    result

                )

        state.selected_tools = (

            selected_tools

        )

        state.tool_selection_result = (

            selected_tools

        )

        return state