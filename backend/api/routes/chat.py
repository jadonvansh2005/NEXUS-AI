from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    Request
)

import os

from agents.core.agent_state import (
    AgentState
)

from memory.memory_manager import (
    MemoryManager
)

from auth.jwt.auth_dependency import (
    get_current_user
)

from database.connection import (
    SessionLocal
)


from memory.fact_memory.fact_manager import (
    FactManager
)

from memory.long_term.memory_service import (
    MemoryService
)

from agents.episodic_router.episodic_router import (
    EpisodicRouter
)

from memory.episodic.episodic_manager import (
    EpisodicManager
)

from agents.memory_router.memory_router import (
    MemoryRouter
)

from agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent
)

router = APIRouter()

agent = OrchestratorAgent()

memory_service = (
    MemoryService()
)

memory_manager = (
    MemoryManager()
)

fact_manager = (
    FactManager()
)

memory_router = (
    MemoryRouter()
)

episodic_manager = (
    EpisodicManager()
)


episodic_router = (
    EpisodicRouter()
)

print("=" * 80, flush=True)
print("CHAT ROUTE ENTERED", flush=True)
print("=" * 80, flush=True)


@router.post("/chat")
async def chat(

    request: Request,

    message: str = Form(...),
    conversation_id: int = Form(None),

    file: UploadFile = File(None),

    current_user=Depends(
        get_current_user
    )

):

    # Dynamic fallback: If file is None, scan all multipart form parameters for any UploadFile
    if not file:
        try:
            form = await request.form()
            for key, value in form.items():
                if isinstance(value, UploadFile) and value.filename:
                    file = value
                    print(f"📧 Dynamic fallback: found uploaded file under parameter '{key}': {file.filename}", flush=True)
                    break
        except Exception as form_err:
            print(f"Error parsing form fields in dynamic fallback: {form_err}", flush=True)

    file_path = ""

    # Dynamic file auto-resolver copy fallback: if no file binary uploaded, parse query and resolve locally
    if not file:
        import re
        import shutil
        file_match = re.search(
            r'(?:attach|file)(?:\s+(?:the|a)?\s*file(?:\s+named)?)?\s+["\']([^"\']+)["\']', 
            message, 
            re.IGNORECASE
        )
        if not file_match:
            file_match = re.search(
                r'(?:attach|file)(?:\s+(?:the|a)?\s*file(?:\s+named)?)?\s+([^,\.\?]+)', 
                message, 
                re.IGNORECASE
            )
        if file_match:
            filename = file_match.group(1).strip()
            # If path was sent (e.g. D:/UPSS/backend/uploads/datasets/Sample of Rubrics.pdf), get just the basename
            filename = os.path.basename(filename)
            if filename and "." in filename:
                search_paths = [
                    os.path.join("D:\\", filename),
                    os.path.join("D:\\UPSS", filename),
                    os.path.join("D:\\UPSS\\backend", filename)
                ]
                # Check uploads recursively
                for root_dir, _, files in os.walk("uploads"):
                    if filename in files:
                        search_paths.append(os.path.join(root_dir, filename))
                        break
                
                for p in search_paths:
                    if os.path.exists(p):
                        dest_dir = "uploads/datasets"
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_path = os.path.join(dest_dir, filename)
                        try:
                            if os.path.abspath(p) != os.path.abspath(dest_path):
                                shutil.copy2(p, dest_path)
                                print(f"📧 Dynamic fallback: copied local file '{p}' to '{dest_path}'", flush=True)
                            file_path = dest_path
                            break
                        except Exception as copy_err:
                            print(f"Error copying local file: {copy_err}", flush=True)
    print("="*50)
    print("FILE OBJECT =", file)
    print("FILE TYPE =", type(file))
    print("="*50)
    if file:
        print("INSIDE FILE BLOCK")
        print(file.filename)

        upload_dir = (
            "uploads/datasets"
        )

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_dir,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            content = await file.read()

            buffer.write(
                content
            )

    db = SessionLocal()
    approved_by_user = False
    rejected_by_user = False

    if message.startswith("Approve: "):
        approved_by_user = True
        message = message[len("Approve: "):]
    elif message.startswith("Reject: "):
        rejected_by_user = True
        message = message[len("Reject: "):]

    if rejected_by_user:
        try:
            conv_id = conversation_id
            if not conv_id:
                conv = memory_service.create_conversation(db=db, user_id=current_user.id, title="Cancelled Task")
                conv_id = conv.id
            
            response_text = "Task execution cancelled by user."
            memory_service.save_message(
                db=db,
                conversation_id=conv_id,
                role="assistant",
                content=response_text
            )
            return {
                "conversation_id": conv_id,
                "domain": "general",
                "response": response_text
            }
        finally:
            db.close()

    try:

        if conversation_id:

            conversation = (

                memory_service.get_conversation(

                    db=db,

                    conversation_id=conversation_id

                )

            )

            if not conversation:

                raise Exception(
                    "Conversation Not Found"
                )

            if conversation.user_id != current_user.id:

                raise Exception(
                    "Unauthorized Conversation"
                )

        else:

            conversation = (

                memory_service.create_conversation(

                    db=db,

                    user_id=current_user.id,

                    title=message[:50]

                )

            )

        state = AgentState(

            user_query=message,

            file_path=file_path,

            user_id=current_user.id,

            email=current_user.email,

            conversation_id=conversation.id

        )
        if approved_by_user:
            state.metadata["approved_by_user"] = True

        memory_service.save_message(

            db=db,

            conversation_id=conversation.id,

            role="user",

            content=message

        )

        # Check if the query is a tool execution request to bypass profile fact hijacking
        q_lower = message.lower()
        has_tool_keywords = any(
            w in q_lower
            for w in [
                "email", "mail", "send", "weather", "temp", "temperature",
                "calculate", "calculator", "math", "distance", "route", "map"
            ]
        )

        extracted_facts = None
        if not has_tool_keywords:
            extracted_facts = fact_manager.process_message(
                db=db,
                user_id=current_user.id,
                message=message
            )

        episodic_manager.process_message(

            db=db,

            user_id=current_user.id,

            message=message

        )

        if extracted_facts:
            confirmations = []
            for key, value in extracted_facts.items():
                key_readable = key.replace("_", " ").title()
                confirmations.append(f"{key_readable} as '{value}'")
            
            response_text = f"Got it! I've saved the following to your profile: {', '.join(confirmations)}."
            
            memory_service.save_message(
                db=db,
                conversation_id=conversation.id,
                role="assistant",
                content=response_text
            )
            
            return {
                "conversation_id": conversation.id,
                "domain": "general",
                "execution_plan": ["Store Fact", "Confirm Storage"],
                "response": response_text
            }

        conversation_context = (

            memory_manager.build_context(

                db=db,

                conversation_id=conversation.id

            )

        )

        fact_context = (

            fact_manager.build_fact_context(

                db=db,

                user_id=current_user.id

            )

        )

        # Get recent episodic memories from database
        events = episodic_manager.service.get_recent_events(db=db, user_id=current_user.id, limit=5)
        episodic_context = ""
        if events:
            event_lines = [f"- {e.event} ({e.created_at.strftime('%Y-%m-%d')})" for e in events]
            episodic_context = "===== PAST EVENTS & MILESTONES =====\n" + "\n".join(event_lines)

        context_parts = []
        if fact_context:
            context_parts.append(fact_context)
        if episodic_context:
            context_parts.append(episodic_context)
        if conversation_context:
            context_parts.append(conversation_context)

        state.memory_context = "\n\n".join(context_parts)

        try:
            # 1. With LLM: run agent execution directly
            result = await agent.execute(
                state
            )
        except Exception as e:
            # 2. Without LLM (Offline fallback / Quota exceeded)
            print(f"[LLM Agent Error - Falling back to offline tool execution] {e}")
            import traceback
            traceback.print_exc()
            
            fallback_response = ""
            detected_domain = "general"
            
            try:
                # Offline tool execution fallback
                from agents.planner.task_decomposer import TaskDecomposer
                from agents.workflow.workflow_executor import WorkflowExecutor
                from agents.planner.schemas import ExecutionPlan
                from agents.domain_detector.classifier import DomainClassifier
                
                detector = DomainClassifier()
                detected_domain = detector.classify(message)
                
                decomposer = TaskDecomposer()
                tasks = decomposer.decompose(message, detected_domain)
                
                if tasks:
                    print(f"[Offline Fallback] Executing tasks offline: {[t.name for t in tasks]}")
                    state.execution_plan = ExecutionPlan(goal=message, domain=detected_domain, tasks=tasks)
                    state.domain = detected_domain
                    
                    from agents.workflow.workflow_agent import WorkflowAgent
                    workflow_agent = WorkflowAgent()
                    state = await workflow_agent.execute(state)
                    
                    tool_outputs = []
                    w_state = getattr(state, "workflow_state", None)
                    if w_state and hasattr(w_state, "results") and w_state.results:
                        for task_id, output_val in w_state.results.items():
                            t_name = next((t.name for t in state.execution_plan.tasks if t.id == task_id), task_id)
                            
                            # Clean up and format tool outputs for offline presentation
                            formatted_val = ""
                            if isinstance(output_val, dict):
                                # 1. Browser Search Output
                                if "search" in output_val and "page" in output_val:
                                    search_data = output_val.get("search", {})
                                    page_data = output_val.get("page", {})
                                    summary = []
                                    if isinstance(search_data, dict) and "results" in search_data:
                                        summary.append("**Search Results:**")
                                        for r in search_data.get("results", [])[:3]:
                                            summary.append(f"- [{r.get('title')}]({r.get('url')}) - *{r.get('snippet')}*")
                                    
                                    # Fix: extract nested page text from BrowserResponse model structure
                                    nested_page = page_data.get("page", {}) if isinstance(page_data, dict) else {}
                                    if nested_page and isinstance(nested_page, dict) and nested_page.get("text"):
                                        text_snippet = nested_page.get("text", "").strip()[:350]
                                        summary.append(f"\n**Scraped Snippet:**\n> {text_snippet}...")
                                    formatted_val = "\n".join(summary) if summary else str(output_val)[:400]
                                
                                # 2. Path-based outputs (Screenshot, Download)
                                elif "path" in output_val:
                                    formatted_val = f"Saved file on your PC: `{output_val['path']}`"
                                
                                # 3. Repository Search Output
                                elif "repositories" in output_val:
                                    summary = ["**Found Repositories:**"]
                                    for r in output_val.get("repositories", [])[:3]:
                                        summary.append(f"- [{r.get('owner')}/{r.get('name')}]({r.get('url')}) (★ {r.get('stars')})")
                                    formatted_val = "\n".join(summary)
                                
                                # 4. Generic Dictionary fallback
                                # 4. Generic Dictionary fallback
                                else:
                                    try:
                                        from agents.reporting_agent.reporting_agent import ReportingAgent

                                        reporter = ReportingAgent()

                                        formatted_val = await reporter.generate_tool_summary(
                                            task_name=t_name,
                                            tool_output=output_val,
                                            user_query=message,
                                        )

                                    except Exception:
                                        formatted_val = str(output_val)
                            else:
                                formatted_val = str(output_val)[:600]
                                
                            if not formatted_val or formatted_val == "[]":
                                if "history" in t_name.lower():
                                    formatted_val = "No visited pages recorded in this session yet."
                                else:
                                    formatted_val = "No data returned."
                                
                            tool_outputs.append(f"### {t_name}\n{formatted_val}")
                    
                    if tool_outputs:

                        from agents.reporting_agent.reporting_agent import ReportingAgent

                        reporter = ReportingAgent()

                        fallback_response = await reporter.generate_offline_response(

                            user_query=message,

                            tool_outputs=tool_outputs,

                            domain=detected_domain,

                        )
            except Exception as offline_err:
                print(f"[Offline Exec Error] {offline_err}")
                traceback.print_exc()
                
            if not fallback_response:
                # 1. Try to extract dynamic RAG context if retrieved from uploaded documents
                rag_content = getattr(state, "context", "")
                if rag_content and "===== DOCUMENT =====" in rag_content:
                    parts = rag_content.split("===== DOCUMENT =====")
                    if len(parts) > 1:
                        chunks_text = parts[1].split("=====")[0].strip()
                        if chunks_text:
                            fallback_response = f"### Offline Mode: Retrieved Document Snippets\n\nHere are the most relevant sections found in your uploaded documents:\n\n{chunks_text}"
                
                if not fallback_response:
                    # Try to match the query directly against MemoryRouter or EpisodicRouter
                    direct_ans = memory_router.try_answer(db=db, user_id=current_user.id, query=message)
                    if not direct_ans:
                        direct_ans = episodic_router.try_answer(db=db, user_id=current_user.id, query=message, conversation_id=conversation.id)
                        
                    if direct_ans:
                        fallback_response = direct_ans
                    else:
                        # Fallback to listing all stored user facts
                        facts_list = fact_manager.service.get_user_facts(db=db, user_id=current_user.id)
                        if facts_list:
                            facts_str = ", ".join([f"{f.fact_key.replace('_', ' ').lower()}: {f.fact_value}" for f in facts_list])
                            fallback_response = f"Stored facts: {facts_str}."
                        else:
                            fallback_response = "I'm currently running in offline mode and I don't have any facts stored in your profile yet."
                
            result = state
            result.final_response = fallback_response
            result.domain = detected_domain
            if not result.execution_plan:
                result.execution_plan = ["LLM Quota Fallback", "Fetch Local Facts"]

        # Check if there is a pending HITL approval paused state
        pending = None

        if (
            hasattr(result, "workflow_state")
            and result.workflow_state
        ):
            pending = result.workflow_state.metadata.get(
                "pending_approval"
            )
        if pending:
            tool_name = pending.get("tool_name", "unknown")
            action = pending.get("action", "execute")
            params = pending.get("parameters", {})
            
            to_val = params.get("to", "")
            subject_val = params.get("subject", "")
            body_val = params.get("body", "")
            dest_val = params.get("destination", "")
            orig_val = params.get("origin", "")
            j_date = params.get("journey_date", "")
            dep_date = params.get("departure_date", "")
            check_in = params.get("check_in", "")
            check_out = params.get("check_out", "")
            b_type = params.get("booking_type", "")
            
            detail_str = f"\n- **Task**: {tool_name}\n- **Action**: {action}"
            if to_val:
                detail_str += f"\n- **To**: {to_val}"
            if subject_val:
                detail_str += f"\n- **Subject**: {subject_val}"
            if body_val:
                detail_str += f"\n- **Body**: {body_val}"
            if dest_val:
                detail_str += f"\n- **Destination**: {dest_val}"
            if orig_val:
                detail_str += f"\n- **Origin**: {orig_val}"
            if j_date and j_date != "None" and j_date != "":
                detail_str += f"\n- **Journey Date**: {j_date}"
            if dep_date and dep_date != "None" and dep_date != "":
                detail_str += f"\n- **Departure Date**: {dep_date}"
            if check_in and check_in != "None" and check_in != "":
                detail_str += f"\n- **Check In**: {check_in}"
            if check_out and check_out != "None" and check_out != "":
                detail_str += f"\n- **Check Out**: {check_out}"
            if b_type:
                detail_str += f"\n- **Booking Type**: {b_type}"
                
            response_text = f"⚠️ **[APPROVAL REQUIRED]**\n\nThe system requires your authorization to perform a high-risk action:\n{detail_str}\n\nDo you approve executing this task?"
            
            memory_service.save_message(
                db=db,
                conversation_id=conversation.id,
                role="assistant",
                content=response_text
            )
            return {
                "conversation_id": conversation.id,
                "domain": result.domain,
                "execution_plan": result.execution_plan,
                "response": response_text,
                "pending_approval": pending
            }

        memory_service.save_message(

            db=db,

            conversation_id=conversation.id,

            role="assistant",

            content=result.final_response

        )

        return {

            "conversation_id":
                conversation.id,

            "domain":
                result.domain,

            "execution_plan":
                result.execution_plan,

            "response":
                result.final_response

        }

    finally:

        db.close()