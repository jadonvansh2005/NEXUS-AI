"""
Workflow Executor

Responsibilities

- Execute scheduled workflow tasks
- Update workflow runtime state
- Coordinate task execution

Future

- Tool Selection Engine
- Execution Controller
- Parallel Execution
- Retry Handling
- Reflection
"""

from __future__ import annotations

import re
from typing import List

from agents.planner.schemas import (
    PlannerTask,
)

from agents.workflow.workflow_models import (
    WorkflowStatus,
    WorkflowTaskStatus,
)

from agents.workflow.workflow_state import (
    WorkflowState,
)


class WorkflowExecutor:

    """
    Executes workflow tasks.

    NOTE

    This class does NOT execute tools directly.

    It only manages workflow execution.

    Tool execution will be delegated to the
    Tool Selection Engine.
    """

    # =====================================================
    # Execute
    # =====================================================

    async def execute(
        self,
        tasks: List[PlannerTask],
        state: WorkflowState,
    ) -> WorkflowState:

        import re
        from agents.tool_selection.tool_selector_agent import ToolSelectorAgent
        from agents.execution.execution_controller import ExecutionController
        from agents.execution.execution_state import ExecutionState
        from tools.register_tools import registry
        from agents.tool_selection.provider_registry import ProviderRegistry

        # Registry and provider setup
        provider_registry = ProviderRegistry()
        for t_name in registry.list_tools():
            meta = registry.get_metadata(t_name)
            if meta and meta.providers:
                provider_registry.register(t_name, meta.providers)

        selector = ToolSelectorAgent(registry, provider_registry)
        controller = ExecutionController()
        
        print(f"[DIAGNOSTIC] Registered tools inside executor: {registry.list_tools()}")

        state.workflow_status = (
            WorkflowStatus.RUNNING
        )

        for task in tasks:

            self._start_task(
                task,
                state,
            )

            # 1. Match and Select Tool for the task
            selection = selector.select_tool(task)
            if selection:
                tool_def = selection["tool"]
                provider = selection["provider"]
                
                # Fetch task parameters
                task_input = task.parameters or {}
                
                # Dynamic parameters fallback for research tasks
                tool_name = getattr(tool_def, "name", "")
                if tool_name == "browser.reader" and not task_input.get("url"):
                    import re
                    user_q = state.metadata.get("user_query", "")
                    url_match = re.search(r'(https?://\S+)', user_q)
                    if url_match:
                        task_input["url"] = url_match.group(1).rstrip('.')
                
                if tool_name == "search.web" and not task_input.get("query"):
                    task_input["query"] = state.metadata.get("user_query", "")

                # Dynamic parameters fallback for coding tasks
                if tool_name == "coding.code_generator":
                    if not task_input.get("prompt"):
                        task_input["prompt"] = state.metadata.get("user_query", "")
                    if not task_input.get("language"):
                        user_q = state.metadata.get("user_query", "").lower()
                        lang = "python"
                        for l in ["javascript", "typescript", "java", "c++", "c#", "html", "css", "go", "rust"]:
                            if l in user_q:
                                lang = l
                                break
                        task_input["language"] = lang
                        
                if tool_name in ["coding.code_reviewer", "coding.code_explainer"]:
                    if not task_input.get("code"):
                        prev_code = ""
                        results = getattr(state, "results", {})
                        for t_id, t_res in results.items():
                            if isinstance(t_res, dict) and "code_generation" in t_res:
                                prev_code = t_res["code_generation"].get("prompt", "")
                            elif isinstance(t_res, str):
                                prev_code = t_res
                        task_input["code"] = prev_code or "print('Hello, World!')"
                    if not task_input.get("language"):
                        task_input["language"] = "python"
                
                # Dynamic parameters fallback for general tools
                if tool_name == "calculator.calculate":
                    if not task_input.get("expression"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        math_match = re.search(r'([0-9\s\+\-\*\/\(\)\.]+)', user_q)
                        task_input["expression"] = math_match.group(1).strip() if math_match else "2 + 2"

                if tool_name in ["weather.current", "weather.air_quality", "weather.alerts", "weather.forecast"]:
                    if not task_input.get("location"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        loc_match = re.search(r'\b(?:in|at|of|for)\b\s+([a-zA-Z\s]+)', user_q, re.IGNORECASE)
                        task_input["location"] = loc_match.group(1).strip() if loc_match else "Delhi"
                    if tool_name == "weather.forecast" and not task_input.get("days"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        days_match = re.search(r'\b(\d+)\s+days\b', user_q, re.IGNORECASE)
                        task_input["days"] = int(days_match.group(1)) if days_match else 3

                if tool_name in ["maps.distance", "maps.navigation", "maps.route"]:
                    if not task_input.get("origin"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        orig_match = re.search(r'(?:from|between)\s+([a-zA-Z\s]+?)\s+(?:to|and)', user_q, re.IGNORECASE)
                        task_input["origin"] = orig_match.group(1).strip() if orig_match else "Delhi"
                    if not task_input.get("destination"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        dest_match = re.search(r'(?:to|and)\s+([a-zA-Z\s]+)', user_q, re.IGNORECASE)
                        task_input["destination"] = dest_match.group(1).strip() if dest_match else "Mumbai"

                if tool_name == "maps.geocode":
                    if not task_input.get("address"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        addr_match = re.search(r'\b(?:geocode|coordinates\s+of|lat\s+long\s+of|location\s+of|for)\b\s+([a-zA-Z0-9\s]+)', user_q, re.IGNORECASE)
                        task_input["address"] = addr_match.group(1).strip() if addr_match else "Delhi"
                        
                if tool_name == "maps.nearby_places":
                    if not task_input.get("location"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        loc_match = re.search(r'\b(?:in|at|near|of|for)\b\s+([a-zA-Z\s]+)', user_q, re.IGNORECASE)
                        task_input["location"] = loc_match.group(1).strip() if loc_match else "Delhi"
                    if not task_input.get("place_type"):
                        import re
                        user_q = state.metadata.get("user_query", "")
                        type_match = re.search(r'\b(restaurant|hotel|hospital|atm|cafe|mall|school|college|bank|shop)s?\b', user_q, re.IGNORECASE)
                        task_input["place_type"] = type_match.group(1).strip() if type_match else "restaurant"
                    if not task_input.get("radius"):
                        task_input["radius"] = 1000

                if tool_name in ["email.send", "email.draft"]:
                    import re
                    user_q = state.metadata.get("user_query", "")
                    
                    if not task_input.get("to"):
                        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_q)
                        task_input["to"] = [email_match.group(0)] if email_match else ["test@example.com"]
                        
                    if not task_input.get("subject"):
                        sub_match = re.search(r'subject\s+(?:is|of|about)?\s*["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["subject"] = sub_match.group(1).strip() if sub_match else "UPSS Notification"
                        
                    if not task_input.get("body"):
                        body_match = re.search(r'body\s+(?:is|of|about)?\s*["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["body"] = body_match.group(1).strip() if body_match else "Hello, this is a message from the UPSS assistant."

                if tool_name in ["email.read", "email.attachment"]:
                    import re
                    user_q = state.metadata.get("user_query", "")
                    if not task_input.get("email_id"):
                        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_q)
                        if email_match:
                            task_input["email_id"] = email_match.group(0).strip()
                        else:
                            id_match = re.search(r'id\s+(\S+)', user_q, re.IGNORECASE)
                            task_input["email_id"] = id_match.group(1).strip() if id_match else "1"
                    if tool_name == "email.attachment" and not task_input.get("download_directory"):
                        task_input["download_directory"] = "downloads"

                if tool_name == "email.search":
                    import re
                    user_q = state.metadata.get("user_query", "")
                    if not task_input.get("query"):
                        q_match = re.search(r'search\s+(?:for|about)?\s*["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["query"] = q_match.group(1).strip() if q_match else "interview"
                    if not task_input.get("limit"):
                        task_input["limit"] = 20
                
                # ==========================================================
                # Parameter Binding for Coding & GitHub Tools
                # ==========================================================
                import os
                from pathlib import Path
                
                user_q = state.metadata.get("user_query", "") if state.metadata else ""
                
                # Resolve active workspace folder
                workspace_path = os.getcwd()
                w_match = re.search(r'\[workspace:\s*(.+?)\]', user_q)
                if w_match:
                    workspace_path = w_match.group(1).strip()

                if tool_name == "coding.code_generator":
                    if not task_input.get("prompt"):
                        task_input["prompt"] = user_q
                    if not task_input.get("language"):
                        lang_match = re.search(r'\b(python|javascript|typescript|html|css|java|c\+\+|cpp|c#|rust|go)\b', user_q, re.IGNORECASE)
                        task_input["language"] = lang_match.group(1).title() if lang_match else "Python"
                    if not task_input.get("framework"):
                        fw_match = re.search(r'\b(django|flask|fastapi|react|nextjs|vue|angular|express|spring|laravel)\b', user_q, re.IGNORECASE)
                        task_input["framework"] = fw_match.group(1).title() if fw_match else None

                elif tool_name == "coding.project_generator":
                    if not task_input.get("project_name"):
                        proj_match = re.search(r'\b(?:project|boilerplate|app|repo|named)\s+([a-zA-Z0-9_\-]+)\b', user_q, re.IGNORECASE)
                        task_input["project_name"] = proj_match.group(1).strip() if proj_match else "my-app"
                    if not task_input.get("description"):
                        task_input["description"] = f"A new project generated by UPSS Assistant."
                    if not task_input.get("language"):
                        lang_match = re.search(r'\b(python|javascript|typescript|html|css|java|c\+\+|cpp|c#|rust|go)\b', user_q, re.IGNORECASE)
                        task_input["language"] = lang_match.group(1).title() if lang_match else "Python"
                    if not task_input.get("framework"):
                        fw_match = re.search(r'\b(django|flask|fastapi|react|nextjs|vue|angular|express|spring|laravel)\b', user_q, re.IGNORECASE)
                        task_input["framework"] = fw_match.group(1).title() if fw_match else None

                elif tool_name == "coding.dependency_analyzer":
                    if not task_input.get("project_path"):
                        task_input["project_path"] = workspace_path

                elif tool_name in ["coding.code_reviewer", "coding.code_explainer", "coding.bug_fixer", "coding.debugger", "coding.refactor", "coding.test_generator", "coding.documentation"]:
                    # Cascade generated code from previous tasks if available
                    prev_code = ""
                    if hasattr(state, "results") and state.results:
                        for prev_res in state.results.values():
                            if isinstance(prev_res, dict) and "code_generation" in prev_res:
                                prev_code = prev_res["code_generation"].get("code", "")
                                break
                    if not task_input.get("code"):
                        task_input["code"] = prev_code if prev_code else "def hello():\n    print('Hello World')\n"
                    if not task_input.get("language"):
                        lang_match = re.search(r'\b(python|javascript|typescript|html|css|java|c\+\+|cpp|c#|rust|go)\b', user_q, re.IGNORECASE)
                        task_input["language"] = lang_match.group(1).title() if lang_match else "Python"
                    if tool_name == "coding.bug_fixer" and not task_input.get("error_message"):
                        task_input["error_message"] = "Fix errors in the code."
                    if tool_name == "coding.debugger" and not task_input.get("stack_trace"):
                        task_input["stack_trace"] = None
                    if tool_name == "coding.refactor" and not task_input.get("objective"):
                        task_input["objective"] = "Clean syntax and improve design."

                elif tool_name == "coding.git_assistant":
                    if not task_input.get("repository_path"):
                        task_input["repository_path"] = workspace_path
                    if not task_input.get("task"):
                        task_input["task"] = user_q

                elif tool_name == "github.clone":
                    if not task_input.get("repository"):
                        repo_match = re.search(r'(https://github\.com/[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-\.]+)', user_q)
                        task_input["repository"] = repo_match.group(1).strip() if repo_match else "https://github.com/octocat/Spoon-Knife.git"
                    if not task_input.get("destination"):
                        task_input["destination"] = str(Path(workspace_path).parent)

                elif tool_name == "github.commit":
                    if not task_input.get("repository_path"):
                        task_input["repository_path"] = workspace_path
                    if not task_input.get("message"):
                        msg_match = re.search(r'\b(?:message|msg|m)\s+["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["message"] = msg_match.group(1).strip() if msg_match else "update codebase"

                elif tool_name == "github.push":
                    if not task_input.get("repository_path"):
                        task_input["repository_path"] = workspace_path
                    if not task_input.get("remote"):
                        task_input["remote"] = "origin"
                    if not task_input.get("branch"):
                        task_input["branch"] = "main"

                elif tool_name == "github.search":
                    if not task_input.get("query"):
                        q_match = re.search(r'search\s+(?:for|about)?\s*["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["query"] = q_match.group(1).strip() if q_match else "ai-agent"
                    if not task_input.get("limit"):
                        task_input["limit"] = 5

                elif tool_name in ["github.pull_request", "github.issue"]:
                    if not task_input.get("repository"):
                        repo_match = re.search(r'\b(?:repo|repository|in)\s+([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-\.]+)\b', user_q, re.IGNORECASE)
                        task_input["repository"] = repo_match.group(1).strip() if repo_match else "vansh/test-repo"
                    if not task_input.get("title"):
                        title_match = re.search(r'title\s+["\']?([^"\']+)["\']?', user_q, re.IGNORECASE)
                        task_input["title"] = title_match.group(1).strip() if title_match else "New integration request"
                    if not task_input.get("body"):
                        task_input["body"] = "Created automatically by UPSS assistant."
                    if tool_name == "github.pull_request":
                        if not task_input.get("head"):
                            task_input["head"] = "main"
                        if not task_input.get("base"):
                            task_input["base"] = "main"
                    elif tool_name == "github.issue":
                        if not task_input.get("labels"):
                            task_input["labels"] = ["bug"]

                # Execute the selected tool using ExecutionController
                task_input["raw_query"] = user_q
                exec_state = ExecutionState()
                exec_result = await controller.execute(
                    tool=tool_def,
                    provider=provider,
                    task_input=task_input,
                    state=exec_state
                )
                
                if exec_result.success:
                    self._complete_task(task, state)
                    # Store task result output in workflow state results
                    if not hasattr(state, "results") or state.results is None:
                        state.results = {}
                    state.results[task.id] = exec_result.output
                else:
                    self.fail_task(task, state, exec_result.error or "Tool execution failed.")
            else:
                # Conceptual tasks (like Analyze Problem) do not require a tool; mark them as completed to allow workflow execution to proceed.
                self._complete_task(task, state)
                if not hasattr(state, "results") or state.results is None:
                    state.results = {}
                state.results[task.id] = f"Conceptual task '{task.name}' completed."

        #
        # Check completion
        #

        if self._workflow_completed(
            state,
        ):

            state.workflow_status = (
                WorkflowStatus.COMPLETED
            )

        return state

    # =====================================================
    # Start Task
    # =====================================================

    def _start_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

    ) -> None:

        state.current_task = (
            task.id
        )

        state.update_status(

            task.id,

            WorkflowTaskStatus.RUNNING,

        )

    # =====================================================
    # Complete Task
    # =====================================================

    def _complete_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

    ) -> None:

        state.update_status(

            task.id,

            WorkflowTaskStatus.COMPLETED,

        )

        state.completed_tasks += 1

    # =====================================================
    # Fail Task
    # =====================================================

    def fail_task(

        self,

        task: PlannerTask,

        state: WorkflowState,

        error: str,

    ) -> None:

        state.update_status(

            task.id,

            WorkflowTaskStatus.FAILED,

        )

        state.failed_tasks += 1

        state.mark_error(

            task.id,

            error,

        )

    # =====================================================
    # Workflow Completion
    # =====================================================

    def _workflow_completed(

        self,

        state: WorkflowState,

    ) -> bool:

        for runtime_task in (

            state.runtime_tasks.values()

        ):

            if runtime_task.status != (

                WorkflowTaskStatus.COMPLETED

            ):

                return False

        return True