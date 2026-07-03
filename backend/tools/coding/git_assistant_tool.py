"""
UPSS Git Assistant Tool

Perform Git-related development workflows.

Future integrations:

- GitHub Module
- Terminal Tool
- Git CLI
- LLM
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
    GitAssistantRequest,
    CodingResponse,
)


class GitAssistantTool(BaseTool):
    """
    Assist with Git workflows.
    """

    metadata = ToolMetadata(

        name="coding.git_assistant",

        display_name="Git Assistant",

        description="Assist with Git development workflows.",

        category=ToolCategory.OTHER,

        tags=[
            "git",
            "github",
            "repository",
            "version-control",
        ],

    )

    permission = ToolPermission.write()

    input_model = GitAssistantRequest

    async def execute(
        self,
        context: ToolContext,
        request: GitAssistantRequest,
    ) -> ToolResult:

        import subprocess
        import os
        from pathlib import Path
        from llm.router.model_router import ModelRouter

        repo_path = Path(request.repository_path)
        success = True
        err_output = ""
        output = ""
        provider = "Git CLI"

        # Check if task is a git command execution request
        task_clean = request.task.strip()
        git_cmds = {"status", "diff", "log", "branch", "remote", "show", "config", "stash", "tag"}
        
        is_cli_cmd = False
        words = task_clean.split()
        first_word = words[0].lower() if words else ""
        
        if first_word == "git":
            is_cli_cmd = True
            cli_args = words[1:]
        elif first_word in git_cmds:
            is_cli_cmd = True
            cli_args = words

        if is_cli_cmd and repo_path.exists():
            try:
                cmd = ["git"] + cli_args
                res = subprocess.run(cmd, cwd=str(repo_path), capture_output=True, text=True, check=True)
                output = res.stdout if res.stdout else "Command executed successfully with no output."
                message = f"Executed git {' '.join(cli_args)} successfully."
            except Exception as e:
                success = False
                err_output = str(e)
                output = getattr(e, "stderr", str(e))
                message = f"Failed to execute git command: {e}"
        else:
            # Fallback to AI git support
            provider = "ModelRouter AI Assistant"
            prompt = f"""
You are an expert Git and version control consultant.
Answer the user's question or assist with the Git workflow task described below.
Provide clear explanation and list any required git shell commands.
Task: {request.task}
Repository Path: {request.repository_path}
"""
            router = ModelRouter()
            try:
                output = router.generate(prompt, request.task, "coding")
                message = "Git assistant advice generated successfully."
            except Exception as e:
                success = False
                output = f"Failed to generate Git advice: {e}"
                message = f"Error consulting Git assistant: {e}"

        result = {
            "repository_path": request.repository_path,
            "task": request.task,
            "status": "completed" if success else "failed",
            "output": output,
            "error": err_output,
            "provider": provider,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "git_assistant": result,
                **response.model_dump(),
            },
        )