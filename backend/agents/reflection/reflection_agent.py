"""
Reflection Agent

Responsibilities

- Orchestrate reflection workflow
- Delegate reflection processing
- Store reflection results

Future

- LLM Self Reflection
- Multi-Agent Reflection
- Reflection Memory
- Continuous Learning
"""

from __future__ import annotations

from agents.core.base_agent import (
    BaseAgent,
)

from agents.core.agent_state import (
    AgentState,
)

from agents.reflection.reflection_manager import (
    ReflectionManager,
)

from agents.reflection.reflection_state import (
    ReflectionState,
)


class ReflectionAgent(

    BaseAgent

):

    """
    Reflection Agent.
    """

    def __init__(

        self,

    ):

        super().__init__(

            "ReflectionAgent"

        )

        self.manager = (

            ReflectionManager()

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: AgentState,

    ) -> AgentState:

        self.log(

            "Starting Reflection Agent"

        )

        #
        # Build Reflection State
        #

        reflection_state = (

            ReflectionState(

                user_id=state.user_id or 0,

                query=state.user_query,

                task_id=state.metadata.get(

                    "task_id",

                    "",

                ),

                tool_name=state.metadata.get(

                    "tool_name",

                    "",

                ),

                provider_name=state.metadata.get(

                    "provider_name",

                    "",

                ),

                execution_success=state.metadata.get(

                    "execution_success",

                    True,

                ),

                execution_time_ms=state.metadata.get(

                    "execution_time_ms",

                    0.0,

                ),

                response=state.response,

            )

        )

        #
        # Process Reflection
        #

        reflection_state = (

            self.manager.process(

                reflection_state

            )

        )

        #
        # Save Reflection Result
        #

        state.metadata[

            "reflection_status"

        ] = (

            reflection_state.status.value

        )

        state.metadata[

            "reflection_type"

        ] = (

            reflection_state.reflection_type.value

        )

        state.metadata[

            "reflection_result"

        ] = (

            reflection_state.result.value

        )

        state.metadata[

            "reflection_confidence"

        ] = (

            reflection_state.confidence.value

        )

        state.metadata[

            "reflection_summary"

        ] = (

            reflection_state.summary

        )

        state.metadata[

            "reflection_recommendation"

        ] = (

            reflection_state.recommendation

        )

        state.metadata[

            "reflection_improvement"

        ] = (

            reflection_state.improvement

        )

        return state