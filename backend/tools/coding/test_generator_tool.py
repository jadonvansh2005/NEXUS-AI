"""
UPSS Test Generator Tool

Generate automated test cases.

Future integrations:

- LLM
- Pytest
- Unittest
- JUnit
- Jest
- Python Runner
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.coding.schemas import (
    TestGeneratorRequest,
    CodingResponse,
)


class TestGeneratorTool(BaseTool):
    """
    Generate automated test cases.
    """

    metadata = ToolMetadata(

        name="coding.test_generator",

        display_name="Test Generator",

        description="Generate automated test cases for source code.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "testing",
            "pytest",
            "unit-test",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = TestGeneratorRequest

    async def execute(
        self,
        context: ToolContext,
        request: TestGeneratorRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter

        prompt = f"""
You are an expert QA and software testing engineer.
Generate comprehensive automated unit tests for the following source code.
Language: {request.language}
Framework: {request.framework or "pytest / standard library unit test framework"}

Provide ONLY the test code file. Do not include markdown code block wraps.

Code:
{request.code}
"""
        router = ModelRouter()
        success = True
        message = "Test suite generated successfully."
        try:
            test_code = router.generate(prompt, request.code, "coding")
            if test_code.startswith("```"):
                lines = test_code.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                test_code = "\n".join(lines)
        except Exception as e:
            success = False
            test_code = f"# Failed to generate tests: {e}"
            message = f"Error during test generation: {e}"

        result = {
            "language": request.language,
            "framework": request.framework,
            "lines_of_code": len(request.code.splitlines()),
            "status": "completed" if success else "failed",
            "test_code": test_code,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "test_generation": result,
                **response.model_dump(),
            },
        )