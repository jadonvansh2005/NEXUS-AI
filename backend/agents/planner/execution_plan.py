"""
Execution Plan Builder

Responsibilities

- Estimate Complexity
- Estimate Risk
- Select Execution Strategy
- Decide Human Approval
- Build Execution Plan
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerTask,
)

from agents.planner.planner_models import (
    ComplexityLevel,
    ExecutionStrategy,
    RiskLevel,
)


class ExecutionPlanBuilder:

    """
    Builds execution plans for the Workflow Engine.
    """

    # =====================================================
    # Complexity
    # =====================================================

    def estimate_complexity(
        self,
        domain: str,
        query: str,
    ) -> ComplexityLevel:

        query = query.lower()

        if any(
            word in query
            for word in [

                "multiple",

                "compare",

                "analyze",

                "optimize",

                "workflow",

                "complete",

                "end to end",

            ]
        ):
            return ComplexityLevel.COMPLEX

        if any(
            word in query
            for word in [

                "book",

                "create",

                "generate",

                "build",

                "search",

                "find",

            ]
        ):
            return ComplexityLevel.MEDIUM

        return ComplexityLevel.SIMPLE

    # =====================================================
    # Risk
    # =====================================================

    def estimate_risk(
        self,
        domain: str,
        query: str,
    ) -> RiskLevel:

        query = query.lower()

        if domain in [

            "finance",

            "healthcare",

            "legal",

        ]:
            return RiskLevel.HIGH

        if any(
            word in query
            for word in [

                "book",

                "cancel",

                "payment",

                "purchase",

                "delete",

                "send",

            ]
        ):
            return RiskLevel.HIGH

        if any(
            word in query
            for word in [

                "modify",

                "update",

                "generate",

            ]
        ):
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    # =====================================================
    # Strategy
    # =====================================================

    def execution_strategy(
        self,
        complexity: ComplexityLevel,
    ) -> ExecutionStrategy:

        if complexity == ComplexityLevel.COMPLEX:

            return ExecutionStrategy.HYBRID

        if complexity == ComplexityLevel.MEDIUM:

            return ExecutionStrategy.SEQUENTIAL

        return ExecutionStrategy.SEQUENTIAL

    # =====================================================
    # HITL
    # =====================================================

    def requires_human_approval(
        self,
        risk: RiskLevel,
    ) -> bool:

        return risk == RiskLevel.HIGH

    # =====================================================
    # Build Plan
    # =====================================================

    def build_execution_plan(
        self,
        goal: str,
        domain: str,
        tasks: List[PlannerTask],
    ) -> ExecutionPlan:

        complexity = self.estimate_complexity(
            domain=domain,
            query=goal,
        )

        risk = self.estimate_risk(
            domain=domain,
            query=goal,
        )

        strategy = self.execution_strategy(
            complexity
        )

        plan = ExecutionPlan(

            goal=goal,

            domain=domain,

            complexity=complexity.value,

            risk=risk.value,

            estimated_cost=0.0,

            estimated_duration=None,

            tasks=tasks,

        )

        #
        # Future
        #
        # plan.strategy = strategy
        #
        # plan.requires_human =
        #     self.requires_human_approval(risk)
        #
        # plan.parallel_groups = ...
        #

        return plan