"""
Planner Prompt

Responsibilities

- Build planner prompts
- Provide instructions to the LLM
- Keep prompt engineering isolated

Future

- Few-shot examples
- Dynamic prompts
- Memory-aware prompts
- Domain-aware prompts
"""

from __future__ import annotations

from agents.planner.schemas import (
    PlanningContext,
)


class PlannerPrompt:

    """
    Builds prompts for the Planner LLM.
    """

    SYSTEM_PROMPT = """
You are the Planner Agent of UPSS.

Your responsibility is ONLY planning.

DO NOT answer the user's question.

DO NOT execute tools.

DO NOT generate the final response.

Your only job is to create an execution plan.

The execution plan must:

1. Understand the user's goal.
2. Break the goal into executable tasks.
3. Order the tasks correctly.
4. Identify dependencies.
5. Select the most appropriate tool or agent.
6. Return ONLY valid JSON.

Never return explanations.

Never return markdown.

Return only JSON.
"""

    def build_prompt(
        self,
        context: PlanningContext,
    ) -> str:

        return f"""
{self.SYSTEM_PROMPT}

User Query:
{context.query}

Detected Domain:
{context.domain}

User Preferences:
{context.preferences}

Memory:
{context.memory}

Metadata:
{context.metadata}

Create an execution plan.
"""