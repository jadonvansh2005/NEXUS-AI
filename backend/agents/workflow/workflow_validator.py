"""
Workflow Validator

Responsibilities

- Validate workflow runtime state
- Validate workflow configuration
- Ensure workflow is executable

Future

- DAG cycle detection
- Parallel execution validation
- Conditional branch validation
- Resource availability validation
"""

from __future__ import annotations

from agents.planner.schemas import (
    ExecutionPlan,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)

from agents.workflow.workflow_models import (
    WorkflowStatus,
)


class WorkflowValidator:

    """
    Validate workflow before execution.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(
        self,
        plan: ExecutionPlan,
        state: WorkflowState,
    ) -> bool:

        if not self._validate_plan(plan):

            return False

        if not self._validate_runtime(state):

            return False

        if not self._validate_task_registration(
            plan,
            state,
        ):

            return False

        return True

    # =====================================================
    # Validate Plan
    # =====================================================

    def _validate_plan(
        self,
        plan: ExecutionPlan,
    ) -> bool:

        if len(plan.tasks) == 0:

            return False

        return True

    # =====================================================
    # Validate Runtime
    # =====================================================

    def _validate_runtime(
        self,
        state: WorkflowState,
    ) -> bool:

        if state.workflow_status not in [

            WorkflowStatus.CREATED,

            WorkflowStatus.READY,

        ]:

            return False

        return True

    # =====================================================
    # Validate Task Registration
    # =====================================================

    def _validate_task_registration(
        self,
        plan: ExecutionPlan,
        state: WorkflowState,
    ) -> bool:

        for task in plan.tasks:

            if task.id not in state.runtime_tasks:

                return False

        return True