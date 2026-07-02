"""
Workflow Executor

Responsibilities

- Execute scheduled workflow tasks
- Update workflow runtime state
- Coordinate task execution

Future

- Tool Selection Engine
- Execution Controller
- Parallel Execution
- Retry Handling
- Reflection
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import (
    PlannerTask,
)

from agents.workflow.workflow_models import (
    WorkflowStatus,
    WorkflowTaskStatus,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


class WorkflowExecutor:

    """
    Executes workflow tasks.

    NOTE

    This class does NOT execute tools directly.

    It only manages workflow execution.

    Tool execution will be delegated to the
    Tool Selection Engine.
    """

    # =====================================================
    # Execute
    # =====================================================

    async def execute(

        self,

        tasks: List[PlannerTask],

        state: WorkflowState,

    ) -> WorkflowState:

        from agents.tool_selection.tool_selector_agent import ToolSelectorAgent
        from agents.execution.execution_controller import ExecutionController
        from agents.execution.execution_state import ExecutionState
        from tools.register_tools import registry
        from agents.tool_selection.provider_registry import ProviderRegistry

        # Registry and provider setup
        provider_registry = ProviderRegistry()
        for t_name in registry.list_tools():
            meta = registry.get_metadata(t_name)
            if meta and meta.providers:
                provider_registry.register(t_name, meta.providers)

        selector = ToolSelectorAgent(registry, provider_registry)
        controller = ExecutionController()

        state.workflow_status = (
            WorkflowStatus.RUNNING
        )

        for task in tasks:

            self._start_task(
                task,
                state,
            )

            # 1. Match and Select Tool for the task
            selection = selector.select_tool(task)
            if selection:
                tool_def = selection["tool"]
                provider = selection["provider"]
                
                # Fetch task parameters
                task_input = task.parameters or {}
                
                # Execute the selected tool using ExecutionController
                exec_state = ExecutionState()
                exec_result = await controller.execute(
                    tool=tool_def,
                    provider=provider,
                    task_input=task_input,
                    state=exec_state
                )
                
                if exec_result.success:
                    self._complete_task(task, state)
                    # Store task result output in workflow state results
                    if not hasattr(state, "results") or state.results is None:
                        state.results = {}
                    state.results[task.id] = exec_result.output
                else:
                    self.fail_task(task, state, exec_result.error or "Tool execution failed.")
            else:
                self.fail_task(task, state, f"No tool found matching task capabilities.")

        #
        # Check completion
        #

        if self._workflow_completed(
            state,
        ):

            state.workflow_status = (
                WorkflowStatus.COMPLETED
            )

        return state

    # =====================================================
    # Start Task
    # =====================================================

    def _start_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

    ) -> None:

        state.current_task = (
            task.id
        )

        state.update_status(

            task.id,

            WorkflowTaskStatus.RUNNING,

        )

    # =====================================================
    # Complete Task
    # =====================================================

    def _complete_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

    ) -> None:

        state.update_status(

            task.id,

            WorkflowTaskStatus.COMPLETED,

        )

        state.completed_tasks += 1

    # =====================================================
    # Fail Task
    # =====================================================

    def fail_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

        error: str,

    ) -> None:

        state.update_status(

            task.id,

            WorkflowTaskStatus.FAILED,

        )

        state.failed_tasks += 1

        state.mark_error(

            task.id,

            error,

        )

    # =====================================================
    # Workflow Completion
    # =====================================================

    def _workflow_completed(

        self,

        state: WorkflowState,

    ) -> bool:

        for runtime_task in (

            state.runtime_tasks.values()

        ):

            if runtime_task.status != (

                WorkflowTaskStatus.COMPLETED

            ):

                return False

        return True