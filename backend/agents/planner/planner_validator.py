"""
Planner Validator

Responsibilities

- Validate execution plans
- Validate planner tasks
- Detect invalid dependencies
- Ensure plan consistency

Future

- Circular dependency detection
- Tool availability validation
- Agent availability validation
"""

from __future__ import annotations

from typing import Set

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerTask,
)


class PlannerValidator:

    """
    Validate planner execution plans.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(
        self,
        plan: ExecutionPlan,
    ) -> bool:

        if not self._validate_tasks(plan.tasks):
            return False

        if not self._validate_dependencies(plan.tasks):
            return False

        return True

    # =====================================================
    # Task Validation
    # =====================================================

    def _validate_tasks(
        self,
        tasks: list[PlannerTask],
    ) -> bool:

        if len(tasks) == 0:
            return False

        ids: Set[str] = set()

        for task in tasks:

            #
            # Duplicate Task ID
            #

            if task.id in ids:
                return False

            ids.add(task.id)

            #
            # Task Name
            #

            if not task.name.strip():
                return False

            #
            # Description
            #

            if not task.description.strip():
                return False

            #
            # Either Tool or Agent will be dynamically resolved during execution
            pass

            #
            # Priority
            #

            if task.priority < 1:
                return False

        return True

    # =====================================================
    # Dependency Validation
    # =====================================================

    def _validate_dependencies(
        self,
        tasks: list[PlannerTask],
    ) -> bool:

        task_ids = {

            task.id

            for task in tasks

        }

        for task in tasks:

            for dependency in task.depends_on:

                if dependency not in task_ids:

                    return False

        return True