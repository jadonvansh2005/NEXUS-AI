"""
Workflow Agent

Responsibilities

- Build runtime workflow
- Validate workflow
- Schedule executable tasks
- Execute workflow
- Update AgentState

Future

- Parallel Execution
- Reflection
- HITL
- Execution Controller
"""

from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState

from agents.workflow.workflow_builder import (
    WorkflowBuilder,
)

from agents.workflow.workflow_validator import (
    WorkflowValidator,
)

from agents.workflow.workflow_scheduler import (
    WorkflowScheduler,
)

from agents.workflow.workflow_executor import (
    WorkflowExecutor,
)

from agents.workflow.workflow_logger import (
    WorkflowLogger,
)

from agents.workflow.workflow_models import (
    WorkflowType,
)


class WorkflowAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "Workflow"
        )

        self.builder = (
            WorkflowBuilder()
        )

        self.validator = (
            WorkflowValidator()
        )

        self.scheduler = (
            WorkflowScheduler()
        )

        self.executor = (
            WorkflowExecutor()
        )

        self.logger = (
            WorkflowLogger()
        )

    # =====================================================
    # Execute
    # =====================================================

    async def execute(
        self,
        state: AgentState,
    ):

        self.log(
            "Workflow Started"
        )

        execution_plan = (
            state.execution_plan
        )

        #
        # No execution plan
        #

        if not execution_plan:

            self.log(
                "No Execution Plan Found"
            )

            return state

        #
        # ----------------------------------------------
        # Build Runtime Workflow
        # ----------------------------------------------
        #

        workflow_state = (
            self.builder.build(
                execution_plan
            )
        )

        workflow_state.metadata["user_query"] = getattr(state, "user_query", "")

        #
        # ----------------------------------------------
        # Validate Workflow
        # ----------------------------------------------
        #

        if not self.validator.validate(

            execution_plan,

            workflow_state,

        ):

            self.log(
                "Workflow Validation Failed"
            )

            return state

        #
        # ----------------------------------------------
        # Logging
        # ----------------------------------------------
        #

        self.logger.workflow_started(
            execution_plan
        )

        #
        # ----------------------------------------------
        # Scheduling Loop
        # ----------------------------------------------
        #

        while True:

            ready_tasks = (

                self.scheduler.schedule(

                    execution_plan,

                    workflow_state,

                    WorkflowType.SEQUENTIAL,

                )

            )

            if len(ready_tasks) == 0:

                break

            self.logger.scheduling(
                len(ready_tasks)
            )

            workflow_state = (

                await self.executor.execute(

                    ready_tasks,

                    workflow_state,

                )

            )

            if workflow_state.failed_tasks > 0:
                self.log("Workflow aborted due to task failure.")
                break

        #
        # ----------------------------------------------
        # Finished
        # ----------------------------------------------
        #

        self.logger.workflow_completed(
            workflow_state
        )

        #
        # Store runtime workflow
        #

        state.workflow_result = (
            workflow_state
        )

        state.workflow_state = (
            workflow_state
        )

        self.log(
            "Workflow Finished"
        )

        return state