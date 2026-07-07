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
                "No dataset uploaded. Please upload a CSV or Excel dataset first."
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

        # Extract details for rich chat bubble presentation
        rows = report.get("dataset_report", {}).get("rows", 0)
        cols = report.get("dataset_report", {}).get("columns", 0)
        
        automl = report.get("automl", {})
        p_type = automl.get("problem_type", "unknown")
        target = automl.get("target", "unknown")
        best = automl.get("best_model", "unknown")
        pdf_path = report.get("pdf_report", "")
        insights = report.get("insights", "")

        # Format Leaderboard table dynamically
        lead_data = automl.get("leaderboard", [])
        leaderboard_rows = []
        
        if isinstance(lead_data, list):
            for idx, item in enumerate(lead_data, 1):
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    model_name, metrics = item
                    primary_val = list(metrics.values())[0] if isinstance(metrics, dict) else metrics
                    leaderboard_rows.append(f"| {idx} | {model_name} | {primary_val} |")
        elif isinstance(lead_data, dict):
            sorted_lead = sorted(
                lead_data.items(), 
                key=lambda x: list(x[1].values())[0] if isinstance(x[1], dict) else x[1], 
                reverse=True
            )
            for idx, (model_name, metrics) in enumerate(sorted_lead, 1):
                primary_val = list(metrics.values())[0] if isinstance(metrics, dict) else metrics
                leaderboard_rows.append(f"| {idx} | {model_name} | {primary_val} |")

        leaderboard_table = ""
        if leaderboard_rows:
            leaderboard_table = "\n### 🏆 Model Leaderboard\n| Rank | Model Name | Primary Score |\n| :--- | :--- | :--- |\n" + "\n".join(leaderboard_rows) + "\n"

        insights_section = ""
        if insights:
            insights_section = f"\n### 💡 Business Insights\n{insights}\n"

        import os
        pdf_abs_path = os.path.abspath(pdf_path) if pdf_path else ""

        state.final_response = (
            f"# 📊 Data Science AutoML Report\n\n"
            f"Successfully executed the automated machine learning pipeline on your dataset!\n\n"
            f"### 📈 Dataset Summary\n"
            f"- **Rows**: {rows}\n"
            f"- **Columns**: {cols}\n\n"
            f"### ⚙️ AutoML Configurations\n"
            f"- **Problem Type**: {p_type}\n"
            f"- **Target Column**: {target}\n"
            f"- **Best Performing Model**: {best}\n"
            f"{leaderboard_table}"
            f"{insights_section}\n"
            f"### 📂 Artifacts Generated\n"
            f"- **AutoML PDF Report**: [Download Report](file:///{pdf_abs_path.replace(os.sep, '/')})\n"
        )

        self.log(
            "Dataset Analysis Complete"
        )

        return state