"""
UPSS Push Tool

Push commits to a remote repository.

Provider-independent implementation.

Future providers:

- Git CLI
- GitPython
- GitHub REST API
- GitHub Enterprise
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

from tools.github.schemas import (
    PushRequest,
    GitHubResponse,
)


class PushTool(BaseTool):
    """
    Push commits to a remote repository.
    """

    metadata = ToolMetadata(

        name="github.push",

        display_name="Git Push",

        description="Push commits to a remote repository.",

        category=ToolCategory.GITHUB,

        tags=[
            "github",
            "git",
            "push",
            "remote",
        ],

    )

    permission = ToolPermission.write()

    input_model = PushRequest

    async def execute(
        self,
        context: ToolContext,
        request: PushRequest,
    ) -> ToolResult:

        import subprocess
        import os
        import httpx
        from pathlib import Path

        repo_path = Path(request.repository_path)
        if not repo_path.exists():
            return ToolResult.error(f"Repository path does not exist: {repo_path}")

        token = os.getenv("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
        success = True
        err_output = ""
        push_status = "success"
        provider = "Git CLI"

        # Check if remote is already configured
        remote_exists = False
        try:
            check_remote = subprocess.run(
                ["git", "remote", "get-url", request.remote],
                cwd=str(repo_path),
                capture_output=True,
                text=True
            )
            if check_remote.returncode == 0:
                remote_exists = True
        except Exception:
            pass

        # If remote does not exist and GITHUB_TOKEN is available, auto-create repository on GitHub
        if not remote_exists and token:
            repo_name = repo_path.name
            print(f"[PushTool] Remote not found. Creating GitHub repository: {repo_name}")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "UPSS-Assistant/1.0"
            }
            payload = {
                "name": repo_name,
                "description": "Repository created automatically by UPSS Developer Assistant.",
                "private": False,
                "auto_init": False
            }
            
            try:
                # 1. Create the repository on GitHub
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post("https://api.github.com/user/repos", json=payload, headers=headers)
                    if resp.status_code in [200, 201]:
                        repo_data = resp.json()
                        clone_url = repo_data.get("clone_url")
                        
                        # Embed token in remote URL for programmatic auth push
                        authed_url = clone_url.replace("https://github.com/", f"https://x-access-token:{token}@github.com/")
                        
                        # 2. Local git initialization
                        subprocess.run(["git", "init"], cwd=str(repo_path), check=True)
                        
                        # Write default .gitignore
                        gitignore_path = repo_path / ".gitignore"
                        if not gitignore_path.exists():
                            with open(gitignore_path, "w") as f:
                                f.write("__pycache__/\n*.pyc\n.env\nvenv/\n.vscode/\n")
                                
                        # Write default README.md
                        readme_path = repo_path / "README.md"
                        if not readme_path.exists():
                            with open(readme_path, "w") as f:
                                f.write(f"# {repo_name}\n\nAutonomous project upload.\n")
                        
                        # Stage and commit initial files
                        subprocess.run(["git", "add", "."], cwd=str(repo_path), check=True)
                        subprocess.run(["git", "commit", "-m", "initial commit"], cwd=str(repo_path), capture_output=True)
                        
                        # Add remote and rename branch
                        subprocess.run(["git", "remote", "add", request.remote, authed_url], cwd=str(repo_path), check=True)
                        subprocess.run(["git", "branch", "-M", request.branch], cwd=str(repo_path), check=True)
                        remote_exists = True
                        provider = "GitHub API + Git CLI"
                    else:
                        success = False
                        err_output = f"GitHub API returned {resp.status_code}: {resp.text}"
            except Exception as e:
                success = False
                err_output = f"Failed to create remote repository: {e}"

        # Run git push command
        if success and remote_exists:
            try:
                cmd = ["git", "push", "-u", request.remote, request.branch]
                res = subprocess.run(cmd, cwd=str(repo_path), capture_output=True, text=True, check=True)
                message = "Repository pushed successfully via Git CLI."
            except Exception as e:
                message = f"Failed to push repository: {e}"
                success = False
                err_output = str(e)
                push_status = "failed"
        else:
            if not token and not remote_exists:
                message = "Failed to push: No remote configured and GITHUB_TOKEN is missing in env."
            else:
                message = f"Failed to push repository: {err_output}"
            success = False
            push_status = "failed"

        push_info = {
            "repository_path": request.repository_path,
            "remote": request.remote,
            "branch": request.branch,
            "status": push_status,
            "provider": provider,
        }

        response = GitHubResponse(
            success=success,
            message=message,
            provider=provider,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "push": push_info,
                "error": err_output,
                **response.model_dump(),
            },
        )