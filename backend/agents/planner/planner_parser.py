"""
Planner Parser

Responsibilities

- Parse LLM planner output
- Convert JSON into Planner schemas
- Validate parser output

Future

- Multiple LLM support
- Retry malformed JSON
- Streaming parser
"""

from __future__ import annotations

import json

from agents.planner.schemas import (
    ExecutionPlan,
    PlannerResult,
    PlannerTask,
)


class PlannerParser:

    """
    Parse planner output into planner objects.
    """

    def parse(
        self,
        response: str,
    ) -> PlannerResult:

        try:

            data = json.loads(response)

        except json.JSONDecodeError:

            return PlannerResult(

                success=False,

                message="Invalid planner response.",

                execution_plan=ExecutionPlan(

                    goal="",

                    domain="general",

                    tasks=[],

                ),

            )

        tasks = []

        for task in data.get("tasks", []):

            tasks.append(

                PlannerTask(

                    id=task.get("id"),

                    name=task.get("name"),

                    description=task.get("description"),

                    tool=task.get("tool"),

                    agent=task.get("agent"),

                    parameters=task.get(
                        "parameters",
                        {},
                    ),

                    depends_on=task.get(
                        "depends_on",
                        [],
                    ),

                    estimated_duration=task.get(
                        "estimated_duration"
                    ),

                    requires_human=task.get(
                        "requires_human",
                        False,
                    ),

                    retryable=task.get(
                        "retryable",
                        True,
                    ),

                    priority=task.get(
                        "priority",
                        1,
                    ),

                )

            )

        plan = ExecutionPlan(

            goal=data.get("goal", ""),

            domain=data.get(
                "domain",
                "general",
            ),

            complexity=data.get(
                "complexity",
                "simple",
            ),

            risk=data.get(
                "risk",
                "low",
            ),

            estimated_cost=data.get(
                "estimated_cost",
                0.0,
            ),

            estimated_duration=data.get(
                "estimated_duration",
            ),

            tasks=tasks,

        )

        return PlannerResult(

            success=True,

            message="Execution plan parsed successfully.",

            execution_plan=plan,

        )