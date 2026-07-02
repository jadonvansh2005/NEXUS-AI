from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
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




@router.post("/chat")
async def chat(

    message: str = Form(...),
    conversation_id: int = Form(None),

    file: UploadFile = File(None),

    current_user=Depends(
        get_current_user
    )

):

    file_path = ""

    if file:

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

        memory_service.save_message(

            db=db,

            conversation_id=conversation.id,

            role="user",

            content=message

        )

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
            print(f"[LLM Agent Error - Falling back to local offline facts] {e}")
            import traceback
            traceback.print_exc()
            
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
            result.domain = "general"
            result.execution_plan = ["LLM Quota Fallback", "Fetch Local Facts"]

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