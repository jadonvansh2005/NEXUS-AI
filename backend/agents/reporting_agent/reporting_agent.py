from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState

# from llm.router.model_router import (
#     ModelRouter
# )

# from llm.prompts.general_prompt import (
#     GENERAL_PROMPT
# )

# from llm.prompts.data_science_prompt import (
#     DATA_SCIENCE_PROMPT
# )


class ReportingAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "ReportingAgent"
        )

        # self.llm = ModelRouter()

    def execute(
        self,
        state: AgentState
    ):

        if state.response:

            state.final_response = state.response

        self.log(
            "Response Generated"
        )

        return state