"""
UPSS Notebook Tool

Executes Jupyter notebooks (.ipynb).
"""

from __future__ import annotations

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.python_runner.schemas import (
    NotebookExecutionRequest,
    NotebookExecutionResponse,
)


class NotebookTool(BaseTool):
    """
    Execute Jupyter notebooks.
    """

    metadata = ToolMetadata(
        name="python.notebook",
        display_name="Notebook Runner",
        description="Execute Jupyter notebooks.",
        category=ToolCategory.CODE_EXECUTION,
        tags=[
            "python",
            "jupyter",
            "notebook",
            "ipynb",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = NotebookExecutionRequest

    async def execute(
        self,
        context: ToolContext,
        request: NotebookExecutionRequest,
    ) -> ToolResult:

        notebook_path = request.path

        timeout = request.timeout

        if not notebook_path.exists():

            response = NotebookExecutionResponse(
                success=False,
                executed_notebook="",
                outputs=[],
                error="Notebook not found.",
            )

            return ToolResult.failure(
                message="Notebook not found.",
                data=response.model_dump(),
            )

        try:

            notebook = nbformat.read(
                notebook_path,
                as_version=4,
            )

            client = NotebookClient(
                notebook,
                timeout=timeout,
                kernel_name="python3",
            )

            client.execute()

            executed_path = notebook_path.with_name(
                notebook_path.stem + "_executed.ipynb"
            )

            nbformat.write(
                notebook,
                executed_path,
            )

            outputs: list[str] = []

            for cell in notebook.cells:

                if cell.cell_type != "code":
                    continue

                for output in cell.get(
                    "outputs",
                    [],
                ):

                    if "text" in output:

                        outputs.append(
                            output["text"]
                        )

                    elif "data" in output:

                        text = output["data"].get(
                            "text/plain"
                        )

                        if text:

                            if isinstance(
                                text,
                                list,
                            ):
                                outputs.extend(text)

                            else:
                                outputs.append(
                                    str(text)
                                )

            response = NotebookExecutionResponse(

                success=True,

                executed_notebook=str(
                    executed_path.resolve()
                ),

                outputs=outputs,

                error=None,

            )

            return ToolResult.ok(

                message="Notebook executed successfully.",

                data=response.model_dump(),

            )

        except CellExecutionError as exc:

            response = NotebookExecutionResponse(

                success=False,

                executed_notebook="",

                outputs=[],

                error=str(exc),

            )

            return ToolResult.failure(

                message="Notebook execution failed.",

                data=response.model_dump(),

            )

        except Exception as exc:

            response = NotebookExecutionResponse(

                success=False,

                executed_notebook="",

                outputs=[],

                error=str(exc),

            )

            return ToolResult.failure(

                message="Notebook execution failed.",

                data=response.model_dump(),

            )