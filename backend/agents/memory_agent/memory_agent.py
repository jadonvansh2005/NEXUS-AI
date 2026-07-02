from agents.core.base_agent import (
    BaseAgent
)

from agents.core.agent_state import (
    AgentState
)

from rag.router.retrieval_router import (
    RetrievalRouter
)

from rag.context.context_builder import (
    ContextBuilder
)

from sqlalchemy.orm import Session

from agents.memory_agent.memory_manager import (
    MemoryManager
)

from agents.memory_agent.memory_state import (
    MemoryState
)


class MemoryAgent(

    BaseAgent

):

    def __init__(

        self

    ):

        super().__init__(

            "MemoryAgent"

        )

        self.memory_manager = (
            MemoryManager()
        )
        

        self.router = (

            RetrievalRouter()

        )

        self.context_builder = (

            ContextBuilder()

        )

        

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: AgentState,

        db: Session = None,

    ) -> AgentState:

        should_close = False
        if db is None:
            from database.connection import SessionLocal
            db = SessionLocal()
            should_close = True

        self.log(

            "Starting Memory Agent"

        )

        # Construct retrieval filters (e.g. filter by user_id to prevent context leaks)
        filters = {}
        if getattr(state, "user_id", None) is not None:
            filters["user_id"] = state.user_id

        retrieval_results = (

            self.router.route(

                query=state.user_query,
                limit=5,
                filters=filters

            )

        )

        rag_context = (

            self.context_builder.build(

                retrieval_results

            )

        )

        # Merge PostgreSQL memory context (facts + conversation history) with Qdrant RAG context
        memory_state = MemoryState(

            user_id=state.user_id,

            query=state.user_query,

        )

        postgres_context = (

            self.memory_manager.retrieve_context(

                db=db,

                state=memory_state,

            )

        )
        context_parts = []
        if postgres_context:
            context_parts.append(f"===== USER PROFILE & HISTORY =====\n{postgres_context}")
        if rag_context:
            context_parts.append(rag_context)

        context = "\n\n".join(context_parts) if context_parts else ""

        state.memory_context = (

            context

        )

        state.context = (

            context

        )

        if should_close:
            db.close()

        return (

            state

        )
    

    