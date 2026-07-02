"""
Capability Matcher

Responsibilities

- Convert planner tasks into capabilities
- Normalize task names
- Prepare capability search

Future

- LLM Capability Extraction
- Embedding Similarity
- Semantic Matching
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import (
    PlannerTask,
)


class CapabilityMatcher:

    """
    Converts planner tasks into required capabilities.
    """

    # =====================================================
    # Public API
    # =====================================================

    def match(
        self,
        task: PlannerTask,
        registry = None,
    ) -> List[str]:

        # 1. Direct registry lookup if the task specifies a tool
        if registry and task.tool:
            try:
                meta = registry.get_metadata(task.tool)
                if meta and meta.capabilities:
                    return meta.capabilities
            except Exception:
                pass

        task_name = task.name.lower()

        capabilities: List[str] = []

        # =================================================
        # Travel
        # =================================================

        if "flight" in task_name:

            capabilities.append(
                "search_flights"
            )

        if "hotel" in task_name:

            capabilities.append(
                "search_hotels"
            )

        if (
            "train" in task_name
            and
            any(
                word in task_name
                for word in (
                    "ticket",
                    "rail",
                    "railway",
                    "station",
                    "journey",
                )
            )
        ):

            capabilities.append(
                "search_trains"
            )

        if "itinerary" in task_name:

            capabilities.append(
                "generate_itinerary"
            )

        if "budget" in task_name:

            capabilities.append(
                "estimate_budget"
            )

        # =================================================
        # Data Science
        # =================================================

        if "dataset" in task_name:

            capabilities.append(
                "load_dataset"
            )

        if "eda" in task_name:

            capabilities.append(
                "perform_eda"
            )

        if (
            "train" in task_name
            and
            any(
                word in task_name
                for word in (
                    "model",
                    "ml",
                    "machine learning",
                    "classifier",
                    "regressor",
                )
            )
        ):

            capabilities.append(
                "train_model"
            )

        if "evaluate" in task_name:

            capabilities.append(
                "evaluate_model"
            )

        if "report" in task_name:

            capabilities.append(
                "generate_report"
            )

        # =================================================
        # Coding
        # =================================================

        if "code" in task_name:

            capabilities.append(
                "generate_code"
            )

        if "review" in task_name:

            capabilities.append(
                "review_code"
            )

        if "debug" in task_name:

            capabilities.append(
                "debug_code"
            )

        if "explain" in task_name:

            capabilities.append(
                "explain_code"
            )

        # =================================================
        # Career
        # =================================================

        if "resume" in task_name:

            capabilities.append(
                "resume_analysis"
            )

        if "ats" in task_name:

            capabilities.append(
                "ats_scoring"
            )

        if "job" in task_name:

            capabilities.append(
                "job_recommendation"
            )

        # =================================================
        # Communication
        # =================================================

        if "message" in task_name:

            capabilities.append(
                "send_message"
            )

        if "email" in task_name:

            capabilities.append(
                "send_email"
            )

        if "translate" in task_name:

            capabilities.append(
                "translation"
            )

        # =================================================
        # Finance
        # =================================================

        if "stock" in task_name:

            capabilities.append(
                "stock_analysis"
            )

        if "portfolio" in task_name:

            capabilities.append(
                "portfolio_analysis"
            )

        if "investment" in task_name:

            capabilities.append(
                "investment_advice"
            )

        # =================================================
        # Default
        # =================================================

        if len(capabilities) == 0:

            capabilities.append(
                "general_assistance"
            )

        return capabilities