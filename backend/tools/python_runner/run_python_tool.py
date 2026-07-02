"""
UPSS Run Python Tool

Executes Python code safely in an isolated Python subprocess.
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.python_runner.schemas import (
    PythonExecutionRequest,
    PythonExecutionResponse,
)


class RunPythonTool(BaseTool):
    """
    Execute Python code in an isolated subprocess.
    """

    metadata = ToolMetadata(
        name="python.run",
        display_name="Run Python",
        description="Execute Python code inside an isolated Python process.",
        category=ToolCategory.CODE_EXECUTION,
        tags=[
            "python",
            "execute",
            "runner",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = PythonExecutionRequest

    async def execute(
        self,
        context: ToolContext,
        request: PythonExecutionRequest,
    ) -> ToolResult:

        previous_directory = None

        try:

            if request.working_directory:

                previous_directory = os.getcwd()

                os.makedirs(
                    request.working_directory,
                    exist_ok=True,
                )

                os.chdir(
                    request.working_directory
                )

            with tempfile.NamedTemporaryFile(

                mode="w",

                suffix=".py",

                delete=False,

                encoding="utf-8",

            ) as script:

                script.write(request.code)

                script_path = script.name

            start = time.perf_counter()

            process = await asyncio.create_subprocess_exec(

                sys.executable,

                script_path,

                stdout=asyncio.subprocess.PIPE,

                stderr=asyncio.subprocess.PIPE,

            )

            try:

                stdout, stderr = await asyncio.wait_for(

                    process.communicate(),

                    timeout=request.timeout,

                )

            except asyncio.TimeoutError:

                process.kill()

                await process.wait()

                return ToolResult.failure(

                    message="Python execution timed out.",

                    data={

                        "timeout": request.timeout,

                    },

                )

            execution_time = (

                time.perf_counter() - start

            )

            response = PythonExecutionResponse(

                success=process.returncode == 0,

                stdout=stdout.decode(
                    "utf-8",
                    errors="replace",
                ),

                stderr=stderr.decode(
                    "utf-8",
                    errors="replace",
                ),

                execution_time=execution_time,

                globals={},

            )

            if response.success:

                return ToolResult.ok(

                    message="Python executed successfully.",

                    data=response.model_dump(),

                )

            return ToolResult.failure(

                message="Python execution failed.",

                data=response.model_dump(),

            )

        finally:

            if previous_directory:

                os.chdir(previous_directory)

            try:

                if "script_path" in locals():

                    Path(script_path).unlink(
                        missing_ok=True,
                    )

            except Exception:
                pass