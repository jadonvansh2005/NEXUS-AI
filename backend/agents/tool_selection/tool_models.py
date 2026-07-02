"""
Tool Selection Models

Responsibilities

- Tool selection enums
- Provider enums
- Tool execution metadata
- Tool selection configuration

Used by

- Tool Selector Agent
- Capability Matcher
- Tool Matcher
- Tool Ranker
- Provider Selector
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Tool Status
# ==========================================================

class ToolStatus(str, Enum):

    AVAILABLE = "available"

    BUSY = "busy"

    DISABLED = "disabled"

    OFFLINE = "offline"


# ==========================================================
# Tool Category
# ==========================================================

class ToolCategory(str, Enum):

    TRAVEL = "travel"

    COMMUNICATION = "communication"

    FINANCE = "finance"

    CODING = "coding"

    DATA_SCIENCE = "data_science"

    CAREER = "career"

    EDUCATION = "education"

    RESEARCH = "research"

    BUSINESS = "business"

    HEALTHCARE = "healthcare"

    LEGAL = "legal"

    PRODUCTIVITY = "productivity"

    SYSTEM = "system"

    GENERAL = "general"


# ==========================================================
# Selection Strategy
# ==========================================================

class SelectionStrategy(str, Enum):

    EXACT_MATCH = "exact_match"

    BEST_MATCH = "best_match"

    CAPABILITY = "capability"

    PROVIDER_PRIORITY = "provider_priority"

    FALLBACK = "fallback"


# ==========================================================
# Provider Status
# ==========================================================

class ProviderStatus(str, Enum):

    ACTIVE = "active"

    DEGRADED = "degraded"

    OFFLINE = "offline"


# ==========================================================
# Tool Confidence
# ==========================================================

class ToolConfidence(str, Enum):

    VERY_HIGH = "very_high"

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"


# ==========================================================
# Tool Configuration
# ==========================================================

class ToolConfiguration(BaseModel):

    enable_fallback: bool = True

    enable_provider_ranking: bool = True

    enable_capability_matching: bool = True

    enable_tool_cache: bool = True

    max_candidate_tools: int = 5

    minimum_confidence: ToolConfidence = (
        ToolConfidence.MEDIUM
    )