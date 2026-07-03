"""
UPSS Code Generator Tool

Generate source code from natural language.

Future integrations:

- LLM
- Project Generator
- File Tool
- GitHub Tool
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
    CodeGeneratorRequest,
    CodingResponse,
)


class CodeGeneratorTool(BaseTool):
    """
    Generate source code from natural language.
    """

    metadata = ToolMetadata(

        name="coding.code_generator",

        display_name="Code Generator",

        description="Generate source code from natural language.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "generator",
            "llm",
            "source-code",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CodeGeneratorRequest

    async def execute(
        self,
        context: ToolContext,
        request: CodeGeneratorRequest,
    ) -> ToolResult:

        from llm.router.model_router import ModelRouter
        import re
        import os
        from pathlib import Path

        # Resolve active workspace path
        workspace_path = os.getcwd()
        q_source = ""
        if context.agent_state and getattr(context.agent_state, "user_query", None):
            q_source = context.agent_state.user_query
        elif context.metadata.get("raw_query"):
            q_source = context.metadata["raw_query"]
        elif request.prompt:
            q_source = request.prompt

        if q_source:
            w_match = re.search(r'\[workspace:\s*(.+?)\]', q_source)
            if w_match:
                workspace_path = w_match.group(1).strip()

        # Parse filename from prompt if present (e.g. save to utils.py or create a file named app.py)
        filename_match = re.search(r'\b(?:create|write\s+to|file|in|save\s+as|named|named\s+as)\b\s+(?:a\s+file\s+)?(?:named\s+)?([a-zA-Z0-9_\-\./]+\.[a-zA-Z0-9_]+)', request.prompt, re.IGNORECASE)
        filename = filename_match.group(1).strip() if filename_match else None

        # Build generation prompt
        prompt = f"""
You are an expert software engineer.
Generate clean, production-ready source code for the following request.
Language: {request.language}
Framework: {request.framework or "None specified"}
Prompt: {request.prompt}

Provide ONLY the code. Do not include markdown code block wraps like ```python or ``` unless explicitly requested.
"""
        router = ModelRouter()
        generated_code = ""
        success = True
        message = "Code generated successfully."

        try:
            generated_code = router.generate(prompt, request.prompt, "coding")
            
            # Clean markdown code block wraps if returned by the LLM
            if generated_code.startswith("```"):
                lines = generated_code.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                generated_code = "\n".join(lines)
        except Exception as e:
            success = False
            message = f"Failed to generate code: {e}"

        # Write to filesystem if a filename was parsed
        file_written = False
        target_file_path = ""
        if success and filename:
            try:
                target_path = Path(workspace_path) / filename
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(generated_code)
                file_written = True
                target_file_path = str(target_path.resolve())
                message = f"Code generated and written successfully to {filename}."
            except Exception as e:
                print(f"[CodeGenerator Error] Failed to write file: {e}")

        result = {
            "prompt": request.prompt,
            "language": request.language,
            "framework": request.framework,
            "status": "success" if success else "failed",
            "code": generated_code,
            "file_written": file_written,
            "file_path": target_file_path,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "code_generation": result,
                **response.model_dump(),
            },
        )