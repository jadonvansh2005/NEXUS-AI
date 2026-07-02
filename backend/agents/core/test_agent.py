from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState


class DummyAgent(BaseAgent):

    def execute(self, state):

        self.log(
            "Executing"
        )

        state.final_response = (
            "Agent Working"
        )

        return state


if __name__ == "__main__":

    state = AgentState(
        user_query="Hello"
    )

    agent = DummyAgent(
        "DummyAgent"
    )

    result = agent.execute(
        state
    )

    print(
        result.final_response
    )