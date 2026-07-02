from agents.core.agent_state import AgentState


class ExecutionController:

    def execute_plan(
        self,
        state: AgentState
    ):

        print(
            "\nExecution Plan:"
        )

        for task in state.execution_plan:

            print(
                f"→ {task}"
            )

        return state