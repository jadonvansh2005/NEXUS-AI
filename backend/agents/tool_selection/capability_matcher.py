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

        if ("code" in task_name and "geocode" not in task_name) or "solution" in task_name:

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

        if "explain" in task_name or "explain solution" in task_name:

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

            if "read" in task_name:
                capabilities.append("read_email")
            elif "search" in task_name:
                capabilities.append("search_email")
            elif "draft" in task_name:
                capabilities.append("draft_email")
            elif "attachment" in task_name or "download" in task_name:
                capabilities.append("download_attachments")
            else:
                capabilities.append("send_email")

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
        # Research & Web
        # =================================================

        if "webpage" in task_name or "read" in task_name or "article" in task_name:

            capabilities.append(
                "read_webpage"
            )

        elif "source" in task_name or "search" in task_name or "collect" in task_name or "research" in task_name:

            capabilities.append(
                "web_search"
            )

        # =================================================
        # Weather
        # =================================================

        if "weather" in task_name or "forecast" in task_name or "temp" in task_name or "aqi" in task_name or "air quality" in task_name or "alert" in task_name:

            if "air quality" in task_name or "aqi" in task_name or "pollution" in task_name:
                capabilities.append("air_quality")
            elif "alert" in task_name or "warning" in task_name:
                capabilities.append("weather_alerts")
            elif "forecast" in task_name or "predict" in task_name or "future" in task_name:
                capabilities.append("weather_forecast")
            else:
                capabilities.append("current_weather")

        # =================================================
        # Maps
        # =================================================

        if "distance" in task_name or "route" in task_name or "map" in task_name or "navigation" in task_name or "geocode" in task_name or "places" in task_name or "nearby" in task_name:

            if "distance" in task_name:
                capabilities.append("map_navigation")
            elif "geocode" in task_name or "coordinates" in task_name:
                capabilities.append("geocode")
            elif "navigation" in task_name or "directions" in task_name:
                capabilities.append("navigation")
            elif "places" in task_name or "nearby" in task_name:
                capabilities.append("nearby_places")
            elif "route" in task_name:
                capabilities.append("route")

        # =================================================
        # Calculator
        # =================================================

        if "calculate" in task_name or "calculator" in task_name or "math" in task_name:

            capabilities.append(
                "calculator"
            )

        # =================================================
        # Default
        # =================================================

        if len(capabilities) == 0:

            capabilities.append(
                "general_assistance"
            )

        return capabilities