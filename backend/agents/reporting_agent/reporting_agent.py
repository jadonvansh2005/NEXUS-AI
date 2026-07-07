# from agents.core.base_agent import BaseAgent
# from agents.core.agent_state import AgentState

# # from llm.router.model_router import (
# #     ModelRouter
# # )

# # from llm.prompts.general_prompt import (
# #     GENERAL_PROMPT
# # )

# # from llm.prompts.data_science_prompt import (
# #     DATA_SCIENCE_PROMPT
# # )


# class ReportingAgent(
#     BaseAgent
# ):

#     def __init__(self):

#         super().__init__(
#             "ReportingAgent"
#         )

#         # self.llm = ModelRouter()

#     def execute(
#         self,
#         state: AgentState
#     ):

#         if state.response:

#             state.final_response = state.response

#         self.log(
#             "Response Generated"
#         )

#         return state
    


from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState

import json


class ReportingAgent(BaseAgent):

    def __init__(self):

        super().__init__("ReportingAgent")

    # =====================================================
    # Existing
    # =====================================================

    def execute(
        self,
        state: AgentState,
    ):

        if state.response:

            state.final_response = state.response

        self.log("Response Generated")

        return state

    # =====================================================
    # Offline Tool Summary
    # =====================================================

    async def generate_tool_summary(
        self,
        task_name: str,
        tool_output,
        user_query: str,
    ) -> str:

        if isinstance(tool_output, dict):

            # ----------------------------
            # Hotels
            # ----------------------------

            if "hotels" in tool_output:

                text = "Here are some hotels I found:\n\n"

                for hotel in tool_output["hotels"][:5]:

                    text += (
                        f"• {hotel['hotel_name']}\n"
                        f"  ⭐ {hotel['rating']}\n"
                        f"  ₹{hotel['price_per_night']} / night\n"
                        f"  📍 {hotel['address']}\n\n"
                    )

                return text

            # ----------------------------
            # Flights
            # ----------------------------

            if "flights" in tool_output:

                text = "Flights found:\n\n"

                for f in tool_output["flights"][:5]:

                    text += (
                        f"• {f.get('airline')}\n"
                        f"₹{f.get('price')}\n\n"
                    )

                return text

            # ----------------------------
            # Search Results
            # ----------------------------

            if "results" in tool_output:

                text = ""

                for r in tool_output["results"][:5]:

                    text += (
                        f"• {r.get('title')}\n"
                        f"{r.get('snippet')}\n\n"
                    )

                return text

        return json.dumps(tool_output, indent=2)

    # =====================================================
    # Final Offline Response
    # =====================================================

    async def generate_offline_response(

        self,

        user_query: str,

        tool_outputs: list,

        domain: str,

    ) -> str:

        response = ""

        if domain == "travel":

            response += "# ✈️ Travel Results\n\n"

        elif domain == "research":

            response += "# 🔍 Research Results\n\n"

        elif domain == "coding":

            response += "# 💻 Coding Results\n\n"

        else:

            response += "# Results\n\n"

        response += "\n\n".join(tool_outputs)

        return response