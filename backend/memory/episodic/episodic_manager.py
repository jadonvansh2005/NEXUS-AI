from datetime import datetime
import uuid
from memory.episodic.episodic_service import (
    EpisodicService
)

from memory.episodic.event_extractor import (
    EventExtractor
)

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    VectorPoint
)


class EpisodicManager:

    def __init__(self):

        self.service = (
            EpisodicService()
        )

        self.extractor = (
            EventExtractor()
        )

        self.embedding_manager = (
            EmbeddingManager(
                model_key="bge_m3"
            )
        )

        self.vector_store = (
            VectorManager()
        )

    def process_message(

        self,

        db,

        user_id: int,

        message: str

    ):

        events = (

            self.extractor.extract(
                message
            )

        )

        for event_type, event in events:

            # 1. Save in PostgreSQL
            self.service.save_event(

                db=db,

                user_id=user_id,

                event_type=event_type,

                event=event

            )

            # 2. Embed and Save in Qdrant Vector DB
            try:
                vector = (
                    self.embedding_manager
                    .embed_query(event)
                )

                point = VectorPoint(
                    id=str(uuid.uuid4()),
                    embedding=vector,
                    payload={
                        "text": event,
                        "user_id": user_id,
                        "event_type": event_type,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )

                self.vector_store.insert(
                    collection_key="episodic",
                    point=point
                )
                print(f"[Episodic Vector Stored] {event} (user_id={user_id})")

            except Exception as e:
                print(f"[Episodic Vector Save Error] {e}")