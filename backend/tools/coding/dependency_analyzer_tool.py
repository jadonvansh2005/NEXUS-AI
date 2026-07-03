"""
UPSS Dependency Analyzer Tool

Analyze project dependencies.

Future integrations:

- pip
- npm
- poetry
- uv
- cargo
- maven
- gradle
- security scanners
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
    DependencyAnalyzerRequest,
    CodingResponse,
)


class DependencyAnalyzerTool(BaseTool):
    """
    Analyze project dependencies.
    """

    metadata = ToolMetadata(

        name="coding.dependency_analyzer",

        display_name="Dependency Analyzer",

        description="Analyze project dependencies.",

        category=ToolCategory.OTHER,

        tags=[
            "coding",
            "dependencies",
            "packages",
            "analysis",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = DependencyAnalyzerRequest

    async def execute(
        self,
        context: ToolContext,
        request: DependencyAnalyzerRequest,
    ) -> ToolResult:

        from pathlib import Path
        import json
        import re

        proj_path = Path(request.project_path)
        dependencies = []
        project_type = "unknown"
        success = True
        message = "Dependency analysis completed successfully."

        if proj_path.exists():
            req_file = proj_path / "requirements.txt"
            pkg_file = proj_path / "package.json"
            
            if req_file.exists():
                project_type = "Python (requirements.txt)"
                try:
                    with open(req_file, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                dependencies.append({"name": line, "type": "pip"})
                except Exception as e:
                    print(f"[DependencyAnalyzer] requirements.txt read error: {e}")
                    
            elif pkg_file.exists():
                project_type = "JavaScript/TypeScript (package.json)"
                try:
                    with open(pkg_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        deps = data.get("dependencies", {})
                        dev_deps = data.get("devDependencies", {})
                        for k, v in deps.items():
                            dependencies.append({"name": k, "version": v, "type": "dependency"})
                        for k, v in dev_deps.items():
                            dependencies.append({"name": k, "version": v, "type": "devDependency"})
                except Exception as e:
                    print(f"[DependencyAnalyzer] package.json read error: {e}")
            else:
                # Scan .py files for standard imports
                project_type = "Python (Static Imports Scan)"
                imports = set()
                try:
                    for file_path in proj_path.rglob("*.py"):
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                match = re.match(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', line)
                                if match:
                                    imports.add(match.group(1))
                    # Exclude standard library helpers to filter external imports
                    stdlib = {
                        "os", "sys", "re", "math", "json", "time", "datetime", "pathlib", 
                        "subprocess", "urllib", "hashlib", "uuid", "collections", "functools", 
                        "typing", "logging", "asyncio", "abc", "random", "shutil"
                    }
                    for imp in sorted(list(imports)):
                        if imp not in stdlib:
                            dependencies.append({"name": imp, "type": "import"})
                except Exception as e:
                    print(f"[DependencyAnalyzer] Import scan error: {e}")
        else:
            success = False
            message = f"Project path does not exist: {proj_path}"

        result = {
            "project_path": str(proj_path.resolve()) if proj_path.exists() else request.project_path,
            "project_type": project_type,
            "status": "completed" if success else "failed",
            "count": len(dependencies),
            "dependencies": dependencies,
        }

        response = CodingResponse(
            success=success,
            message=message,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "dependency_analysis": result,
                **response.model_dump(),
            },
        )