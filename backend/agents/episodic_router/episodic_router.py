from memory.episodic.episodic_service import (
    EpisodicService
)
from memory.long_term.memory_service import (
    MemoryService
)
from rag.embeddings.embedding_manager import (
    EmbeddingManager
)
from rag.vector_store.vector_manager import (
    VectorManager
)


class EpisodicRouter:

    def __init__(self):

        self.service = (
            EpisodicService()
        )
        self.memory_service = (
            MemoryService()
        )
        self.embedding_manager = (
            EmbeddingManager(
                model_key="bge_m3"
            )
        )
        self.vector_store = (
            VectorManager()
        )

    def try_answer(

        self,

        db,

        user_id: int,

        query: str,

        conversation_id: int = None

    ):

        query_lower = query.lower()

        # Check if the query is asking about what was discussed/talked/completed/done last time/yesterday
        is_discussion_query = any(kw in query_lower for kw in [
            "discuss", "talk", "complete", "do last time", "stop", "yesterday", "last topic", "last session", "previous conversation", "progress"
        ]) and any(time_kw in query_lower for time_kw in [
            "last", "yesterday", "previous", "before", "stop", "did we", "we did", "we discuss", "last time"
        ])

        # Semantic Episodic Memory Retrieval
        is_past_query = any(kw in query_lower for kw in [
            "did we", "did i", "have we", "what did we", "where did we", "what we discussed", "what did we do",
            "yesterday", "last week", "last time", "before", "upload", "history", "cuda"
        ]) or is_discussion_query

        if is_past_query:
            try:
                # 1. Embed query and search in Qdrant's episodic collection
                vector = self.embedding_manager.embed_query(query)
                results = self.vector_store.search(
                    collection_key="episodic",
                    query_vector=vector,
                    limit=5,
                    score_threshold=0.6,
                    filters={"user_id": user_id}
                )
                if results:
                    events_list = []
                    for res in results:
                        payload = res.payload
                        text = payload.get("text", "")
                        timestamp = payload.get("timestamp", "")
                        if timestamp:
                            timestamp = timestamp.split("T")[0]
                        events_list.append(f"- {text} ({timestamp})")
                    
                    semantic_response = "Yes, based on your history, we discussed or did the following:\n" + "\n".join(events_list)
                    return semantic_response
            except Exception as e:
                print(f"[Semantic Episodic Retrieval Error] {e}")

        # Fallback to PostgreSQL specific checks if no semantic vector match was found
        if is_discussion_query:
            # Fetch latest event from PostgreSQL
            latest_event = self.service.get_latest_event(db=db, user_id=user_id)
            event_text = f"Yes, we discussed that! The last recorded event is: {latest_event.event}." if latest_event else ""

            # Fetch last user/assistant messages from PostgreSQL messages table
            history_text = ""
            if conversation_id:
                recent_msgs = self.memory_service.get_recent_messages(db=db, conversation_id=conversation_id, limit=5)
                prior_msgs = [m for m in recent_msgs if m.content.strip().lower() != query.strip().lower()][-3:]
                if prior_msgs:
                    history_lines = []
                    for m in prior_msgs:
                        role_label = "You" if m.role == "user" else "AI"
                        history_lines.append(f"{role_label}: {m.content}")
                    history_text = "Recent chat history:\n" + "\n".join(history_lines)

            parts = []
            if event_text:
                parts.append(event_text)
            if history_text:
                parts.append(history_text)

            if parts:
                return "\n\n".join(parts)

        # -------------------------
        # Technology Decisions
        # -------------------------
        latest_decision = (
            self.service.get_latest_decision(
                db=db,
                user_id=user_id
            )
        )
        if latest_decision:
            if (
                "which database did we choose" in query_lower
                or
                "what database did we choose" in query_lower
                or
                "which db did we choose" in query_lower
                or
                "which technology did we choose" in query_lower
                or
                "what tech stack did we choose" in query_lower
            ):
                return f"Latest technology decision: {latest_decision.event}"

        # -------------------------
        # Current Phase
        # -------------------------
        latest_milestone = (
            self.service.get_latest_milestone(
                db=db,
                user_id=user_id
            )
        )
        if latest_milestone:
            if (
                "current phase" in query_lower
                or
                "what phase are we in" in query_lower
                or
                "where are we now" in query_lower
            ):
                return f"Current phase: {latest_milestone.event}"

        return None