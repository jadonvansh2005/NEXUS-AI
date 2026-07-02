"""
UPSS Tool SDK - Tool Discovery

Automatically discovers every tool inside the tools package
and registers it into the ToolRegistry.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import List, Type

from agents.core.tool_registry import ToolRegistry
from tools.base_tool import BaseTool

from agents.tool_selection.provider_registry import (
    ProviderRegistry,
)


class ToolDiscovery:
    """
    Automatically discovers all BaseTool subclasses.
    """

    def __init__(

        self,

        registry: ToolRegistry,

        provider_registry: ProviderRegistry,

    ):

        self.registry = registry

        self.provider_registry = provider_registry

    def discover(
        self,
        package: str = "tools",
        package_path: str | None = None,
    ) -> int:
        """
        Discover and register all tools.

        Returns:
            Number of discovered tools.
        """

        if package_path is None:
            package_path = str(Path(__file__).parent)

        discovered = 0

        for module in pkgutil.walk_packages(
            [package_path],
            prefix=f"{package}.",
        ):

            module_name = module.name

            try:

                imported_module = importlib.import_module(module_name)

            except Exception:
                # Ignore modules that fail to import
                continue

            for _, obj in inspect.getmembers(
                imported_module,
                inspect.isclass,
            ):

                if (
                    issubclass(obj, BaseTool)
                    and obj is not BaseTool
                ):

                    try:

                        tool = obj()

                        self.registry.register_tool(

                            name=tool.name,

                            tool=tool,

                            domain=tool.domain,

                            capabilities=tool.capabilities,

                            providers=tool.providers,

                            enabled=tool.enabled,

                        )

                        self.provider_registry.register(

                            tool_name=tool.name,

                            providers=tool.providers,

                        )
                        discovered += 1

                    except Exception:
                        continue

        return discovered