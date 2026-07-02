"""
UPSS Python Environment Tool

Provides information about the current Python environment.
"""

from __future__ import annotations

import os
import platform
import site
import subprocess
import sys

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)


class EnvironmentTool(BaseTool):
    """
    Inspect the current Python execution environment.
    """

    metadata = ToolMetadata(
        name="python.environment",
        display_name="Python Environment",
        description="Retrieve information about the current Python environment.",
        category=ToolCategory.CODE_EXECUTION,
        tags=[
            "python",
            "environment",
            "venv",
            "packages",
        ],
    )

    permission = ToolPermission.read_only()

    async def execute(
        self,
        context: ToolContext,
        request: dict | None = None,
    ) -> ToolResult:

        request = request or {}

        include_packages = request.get(
            "include_packages",
            False,
        )

        packages = []

        if include_packages:

            try:

                result = subprocess.run(

                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "list",
                        "--format=json",
                    ],

                    capture_output=True,

                    text=True,

                    check=True,

                )

                packages = result.stdout

            except Exception as exc:

                packages = str(exc)

        data = {

            "python_version": sys.version,

            "python_executable": sys.executable,

            "platform": platform.platform(),

            "platform_system": platform.system(),

            "platform_release": platform.release(),

            "architecture": platform.machine(),

            "implementation": platform.python_implementation(),

            "prefix": sys.prefix,

            "base_prefix": getattr(
                sys,
                "base_prefix",
                sys.prefix,
            ),

            "virtual_environment": (
                sys.prefix
                != getattr(
                    sys,
                    "base_prefix",
                    sys.prefix,
                )
            ),

            "working_directory": os.getcwd(),

            "site_packages": site.getsitepackages(),

            "environment_variables": {

                "PATH": os.getenv("PATH"),

                "PYTHONPATH": os.getenv("PYTHONPATH"),

                "VIRTUAL_ENV": os.getenv("VIRTUAL_ENV"),

            },

            "installed_packages": packages,

        }

        return ToolResult.ok(

            message="Python environment retrieved successfully.",

            data=data,

        )