"""
UPSS Project Generator Tool

Generate software project structures.

Future integrations:

- LLM
- Cookiecutter
- Template Engine
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
    ProjectGeneratorRequest,
    CodingResponse,
)


class ProjectGeneratorTool(BaseTool):
    """
    Generate software project structures.
    """

    metadata = ToolMetadata(

        name="coding.project_generator",

        display_name="Project Generator",

        description="Generate software project structures.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "project",
            "generator",
            "template",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ProjectGeneratorRequest

    async def execute(
        self,
        context: ToolContext,
        request: ProjectGeneratorRequest,
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

        if q_source:
            w_match = re.search(r'\[workspace:\s*(.+?)\]', q_source)
            if w_match:
                workspace_path = w_match.group(1).strip()

        project_dir = Path(workspace_path) / request.project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Generate main program boilerplate via LLM
        prompt = f"""
You are an expert software engineer.
Generate a working starter boilerplate entry point file for the following project.
Project Name: {request.project_name}
Description: {request.description}
Language: {request.language}
Framework: {request.framework or "None specified"}

Provide ONLY the code contents of the file. Do not include markdown code block wraps.
"""
        router = ModelRouter()
        success = True
        message = "Project generated successfully."
        
        try:
            main_code = router.generate(prompt, request.description, "coding")
            if main_code.startswith("```"):
                lines = main_code.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                main_code = "\n".join(lines)
        except Exception as e:
            main_code = f"# Starter boilerplate for {request.project_name}\nprint('Hello World')\n"
            success = False
            message = f"Failed to generate boilerplate code via LLM: {e}"

        # Write files
        try:
            readme_content = f"# {request.project_name}\n\n{request.description}\n\n## Structure\n- `README.md`\n- `.gitignore`\n- Main source file\n"
            with open(project_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)

            gitignore_content = "__pycache__/\n*.pyc\nvenv/\nnode_modules/\n.env\n"
            with open(project_dir / ".gitignore", "w", encoding="utf-8") as f:
                f.write(gitignore_content)

            # Determine file extension based on language
            lang_exts = {
                "python": "py", "javascript": "js", "typescript": "ts", 
                "html": "html", "java": "java", "c++": "cpp", "c#": "cs"
            }
            ext = lang_exts.get(request.language.lower(), "txt")
            main_filename = f"main.{ext}" if ext != "html" else "index.html"
            
            with open(project_dir / main_filename, "w", encoding="utf-8") as f:
                f.write(main_code)
                
            message = f"Project '{request.project_name}' generated successfully with README, .gitignore and {main_filename}."
            success = True
        except Exception as e:
            success = False
            message = f"Failed to write project files: {e}"

        result = {
            "project_name": request.project_name,
            "description": request.description,
            "language": request.language,
            "framework": request.framework,
            "status": "success" if success else "failed",
            "path": str(project_dir.resolve()),
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "project": result,
                **response.model_dump(),
            },
        )