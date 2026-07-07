"""
Execution Dispatcher

Responsibilities

- Dispatch execution to selected tools
- Invoke tool execution
- Capture execution result

Future

- Async Dispatch
- Distributed Workers
- Streaming Execution
- Remote MCP Execution
"""

from __future__ import annotations

from typing import Any
from typing import Dict


class ExecutionDispatcher:

    """
    Dispatches execution to the selected tool.
    """

    # =====================================================
    # Public API
    # =====================================================

    async def dispatch(

        self,

        tool_metadata: Any,

        task_input: Dict[str, Any],

    ) -> Any:

        #
        # Retrieve tool instance (supporting both ToolDefinition model and dict)
        #
        from agents.core.tool_definition import ToolDefinition
        if isinstance(tool_metadata, ToolDefinition):
            tool = tool_metadata.metadata.get("instance")
        else:
            tool = tool_metadata.get("tool") if hasattr(tool_metadata, "get") else None

        if tool is None:

            raise ValueError(

                "No tool instance found."

            )

        #
        # Verify execute()
        #

        if not hasattr(

            tool,

            "execute",

        ):

            raise AttributeError(

                f"{tool.__class__.__name__} "
                "does not implement execute()."

            )

        #
        # Dispatch execution (handle both async BaseTool and legacy sync stubs)
        #
        import inspect
        from tools.tool_context import ToolContext
        context = ToolContext()
        if isinstance(task_input, dict) and "raw_query" in task_input:
            context.metadata["raw_query"] = task_input["raw_query"]

        # Parse request model if defined on the tool
        input_model = getattr(tool, "input_model", None)
        if input_model:
            try:
                # If task_input has a nested parameters structure or is flat
                if "parameters" in task_input and hasattr(input_model, "parameters"):
                    request = input_model(**task_input)
                else:
                    # Try to bind directly
                    request = input_model(**task_input)
            except Exception:
                # Fallback to default instantiation
                request = input_model()
        else:
            request = task_input

        # Initialize tool if supported
        if hasattr(tool, "initialize"):
            await tool.initialize()

        try:
            if inspect.iscoroutinefunction(tool.execute):
                result = await tool.execute(context, request)
                if hasattr(result, "data"):
                    return result.data
                return result
            else:
                return tool.execute(task_input)
        finally:
            # Shutdown tool if supported
            if hasattr(tool, "shutdown"):
                await tool.shutdown()

    # =====================================================
    # Batch Dispatch
    # =====================================================

    async def dispatch_batch(

        self,

        tool_metadata: Dict[str, Any],

        inputs: list,

    ) -> list:

        results = []

        for task_input in inputs:

            results.append(

                await self.dispatch(

                    tool_metadata,

                    task_input,

                )

            )

        return results