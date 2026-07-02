"""
Planner Agent

Responsibilities

- Receive AgentState
- Decompose user query
- Build execution plan
- Validate plan
- Prepare plan for Workflow Engine
"""

from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState

from agents.planner.task_decomposer import (
    TaskDecomposer,
)

from agents.planner.execution_plan import (
    ExecutionPlanBuilder,
)

from agents.planner.planner_validator import (
    PlannerValidator,
)

from agents.planner.planner_executor import (
    PlannerExecutor,
)


class PlannerAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Planner"
        )

        self.decomposer = (
            TaskDecomposer()
        )

        self.plan_builder = (
            ExecutionPlanBuilder()
        )

        self.validator = (
            PlannerValidator()
        )

        self.executor = (
            PlannerExecutor()
        )

    def execute(
        self,
        state: AgentState
    ):

        self.log(
            "Planner Started"
        )

        #
        # Read Input
        #

        query = (
            state.user_query
        )

        domain = (
            state.domain
        )

        #
        # ------------------------------------------
        # Task Decomposition
        # ------------------------------------------
        #

        tasks = (
            self.decomposer.decompose(

                query=query,

                domain=domain,

            )
        )

        #
        # ------------------------------------------
        # Build Execution Plan
        # ------------------------------------------
        #

        execution_plan = (
            self.plan_builder.build_execution_plan(

                goal=query,

                domain=domain,

                tasks=tasks,

            )
        )

        #
        # ------------------------------------------
        # Validate Plan
        # ------------------------------------------
        #

        if not self.validator.validate(
            execution_plan
        ):

            self.log(
                "Planner Validation Failed"
            )

            return state

        #
        # ------------------------------------------
        # Planner Executor
        # ------------------------------------------
        #

        planner_result = (
            self.executor.execute(
                execution_plan
            )
        )

        #
        # Store Result
        #

        state.planner_result = planner_result

        state.execution_plan = (
            planner_result.execution_plan
        )

        self.log(

            f"Plan Created: "

            f"{len(execution_plan.tasks)} Tasks"

        )

        return state