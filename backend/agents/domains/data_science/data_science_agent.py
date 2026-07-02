from agents.core.base_agent import (
    BaseAgent
)

from agents.core.agent_state import (
    AgentState
)

from services.data_science_service import (
    DataScienceService
)


class DataScienceAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "DataScienceAgent"
        )

        self.service = (
            DataScienceService()
        )

    def execute(
        self,
        state: AgentState
    ):

        self.log(
            "Executing Data Science Workflow"
        )

        if not state.file_path:

            state.final_response = (
                "No dataset uploaded."
            )

            return state

        report = (

            self.service.analyze_dataset(

                state.file_path

            )

        )

        state.tool_outputs[
            "dataset_analysis"
        ] = report

        self.log(
            "Dataset Analysis Complete"
        )

        return state