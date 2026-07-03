from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import ToolCategory, ToolMetadata
from pydantic import BaseModel

class CalculatorInput(BaseModel):
    expression: str

class CalculatorTool(BaseTool):
    metadata = ToolMetadata(
        name="calculator.calculate",
        display_name="Calculator",
        description="Evaluates a mathematical expression safely.",
        category=ToolCategory.PRODUCTIVITY,
        tags=["calculator", "math", "eval"]
    )
    permission = ToolPermission.read_only()
    input_model = CalculatorInput

    async def execute(self, context: ToolContext, request: CalculatorInput) -> ToolResult:
        expr = request.expression
        # Clean expression to allow only safe mathematical characters
        clean_expr = "".join(c for c in expr if c in "0123456789+-*/(). ")
        try:
            # Safely evaluate mathematical expressions without builtins
            val = eval(clean_expr, {"__builtins__": None}, {})
            return ToolResult.ok(message="Calculation successful.", data={"result": val})
        except Exception as e:
            return ToolResult.failure(message=f"Failed to evaluate expression: {e}")
