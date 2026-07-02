"""
UPSS Install Package Tool

Installs Python packages into the active environment.
"""

from __future__ import annotations

import sys

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.python_runner.schemas import (
    PackageInstallRequest,
    PackageInstallResponse,
)

from tools.terminal.schemas import (
    TerminalRequest,
    ShellType,
)

from tools.terminal.process_manager import (
    ProcessManager,
)


class InstallPackageTool(BaseTool):
    """
    Install Python packages using pip.
    """

    metadata = ToolMetadata(
        name="python.install_package",
        display_name="Install Python Package",
        description="Install Python packages using pip.",
        category=ToolCategory.CODE_EXECUTION,
        tags=[
            "python",
            "pip",
            "install",
            "package",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = PackageInstallRequest

    async def execute(
        self,
        context: ToolContext,
        request: PackageInstallRequest,
    ) -> ToolResult:

        command = (
            f'"{sys.executable}" -m pip install '
            + " ".join(request.packages)
        )

        terminal_request = TerminalRequest(

            command=command,

            shell=ShellType.POWERSHELL,

            timeout=request.timeout,

            working_directory=request.working_directory,

        )

        response = await ProcessManager.execute(
            terminal_request
        )

        install_response = PackageInstallResponse(

            success=response.success,

            installed_packages=request.packages,

            stdout=response.stdout,

            stderr=response.stderr,

            exit_code=response.exit_code,

        )

        if response.success:

            return ToolResult.ok(

                message="Package installation completed.",

                data=install_response.model_dump(),

            )

        return ToolResult.failure(

            message="Package installation failed.",

            data=install_response.model_dump(),

        )