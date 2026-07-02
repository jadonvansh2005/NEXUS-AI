"""
Tool Definition

Canonical representation of every executable tool
available in the UPSS platform.

Responsibilities

- Describe a tool
- Describe supported capabilities
- Describe available providers
- Store execution metadata

This model is the single source of truth for the
Tool Registry.
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ToolDefinition(BaseModel):

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    name: str

    domain: str

    description: str = ""

    # --------------------------------------------------
    # Matching
    # --------------------------------------------------

    capabilities: List[str] = Field(
        default_factory=list
    )

    # --------------------------------------------------
    # Providers
    # --------------------------------------------------

    providers: List[str] = Field(
        default_factory=list
    )

    default_provider: Optional[str] = None

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    execution_class: Optional[str] = None

    enabled: bool = True

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )