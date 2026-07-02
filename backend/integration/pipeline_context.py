"""
Pipeline Context

Responsibilities

- Provide shared services
- Provide shared registries
- Provide shared configuration
- Dependency Injection Container

Notes

- Does NOT create services.
- Only stores references.
- Services are injected during startup.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class PipelineContext:

    # =====================================================
    # Core Services
    # =====================================================

    planner: Optional[Any] = None

    memory_gateway: Optional[Any] = None

    workflow: Optional[Any] = None

    agent_generator: Optional[Any] = None

    tool_selector: Optional[Any] = None

    execution_controller: Optional[Any] = None

    reflection: Optional[Any] = None

    validator: Optional[Any] = None

    hitl: Optional[Any] = None

    response_generator: Optional[Any] = None

    memory_writer: Optional[Any] = None

    # =====================================================
    # Registries
    # =====================================================

    tool_registry: Optional[Any] = None

    agent_registry: Optional[Any] = None

    stage_registry: Optional[Any] = None

    # =====================================================
    # Infrastructure
    # =====================================================

    llm_router: Optional[Any] = None

    model_router: Optional[Any] = None

    database: Optional[Any] = None

    cache: Optional[Any] = None

    event_bus: Optional[Any] = None

    configuration: Dict[str, Any] = field(

        default_factory=dict

    )

    # =====================================================
    # Runtime Services
    # =====================================================

    runtime_services: Dict[str, Any] = field(

        default_factory=dict

    )

    # =====================================================
    # Register
    # =====================================================

    def register(

        self,

        name: str,

        service: Any,

    ) -> None:

        self.runtime_services[

            name

        ] = service

    # =====================================================
    # Resolve
    # =====================================================

    def resolve(

        self,

        name: str,

    ) -> Optional[Any]:

        return self.runtime_services.get(

            name

        )

    # =====================================================
    # Exists
    # =====================================================

    def contains(

        self,

        name: str,

    ) -> bool:

        return (

            name

            in

            self.runtime_services

        )

    # =====================================================
    # Remove
    # =====================================================

    def unregister(

        self,

        name: str,

    ) -> None:

        self.runtime_services.pop(

            name,

            None,

        )