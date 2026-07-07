from abc import ABC
import re
from datetime import datetime

from typing import Dict
from typing import List
from typing import Optional
from typing import Any

from rag.embeddings.embedding_manager import (
    EmbeddingManager
)

from rag.vector_store.vector_manager import (
    VectorManager
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class BaseRetrieval(

    ABC

):

    # Global memory cache for latest uploaded files
    # Key: (user_id, collection_key) -> filename
    _latest_uploads = {}

    def __init__(

        self,

        collection_key: str

    ):

        self.collection_key = (

            collection_key

        )

        self.embedding_manager = (

            EmbeddingManager()

        )

        self.vector_manager = (

            VectorManager()

        )

    # --------------------------------------------------
    # Generic Search
    # --------------------------------------------------

    def search(

        self,

        query: str,

        limit: int = 5,

        score_threshold: Optional[float] = None,

        filters: Optional[

            Dict[str, Any]

        ] = None

    ) -> List[SearchResult]:

        if filters is None:
            filters = {}

        # Context-aware latest file scoping filter
        query_lower = query.lower()
        file_pointers = ["this file", "this pdf", "this document", "the file", "the pdf", "the document", "uploaded file", "uploaded pdf", "uploaded document"]
        if any(ptr in query_lower for ptr in file_pointers):
            user_id = filters.get("user_id")
            if user_id:
                latest_doc_id = self.get_latest_uploaded_file(user_id)
                if latest_doc_id:
                    print(f"[{self.__class__.__name__}] Scoping search strictly to latest document ID: {latest_doc_id}", flush=True)
                    filters["document_id"] = latest_doc_id

        print("\n" + "=" * 80)
        print("[BaseRetrieval] Starting Retrieval")
        print("=" * 80)

        print(f"[Query] {query}")
        print(f"[Collection] {self.collection_key}")
        print(f"[Limit] {limit}")
        print(f"[Score Threshold] {score_threshold}")
        print(f"[Filters] {filters}")

        print("\n[Embedding] Generating query embedding...")

        embedding = (

            self.embedding_manager.embed_query(

                query

            )

        )

        print(f"[Embedding] Dimension = {len(embedding)}")

        print("\n[Vector Search] Searching collection...")

        results = (

            self.vector_manager.search(

                collection_key=self.collection_key,

                query_vector=embedding,

                limit=limit,

                score_threshold=score_threshold,

                filters=filters

            )

        )

        print(f"[Vector Search] Retrieved {len(results)} result(s)\n")

        if not results:

            print("⚠️  No vectors matched this query.")

        else:

            for index, result in enumerate(results, start=1):

                print("-" * 80)
                print(f"Result #{index}")
                print(f"Score : {result.score}")

                if result.payload:

                    print(f"Payload Keys : {list(result.payload.keys())}")

                    text = result.payload.get("text", "")

                    if text:

                        print("\nChunk Preview:")
                        print(text[:300])

                else:

                    print("Payload : None")

        print("=" * 80)
        print("[BaseRetrieval] Retrieval Finished")
        print("=" * 80 + "\n")

        return results

    def get_latest_uploaded_file(self, user_id: int) -> Optional[str]:
        # 1. Try memory cache first
        cache_key = (user_id, self.collection_key)
        if cache_key in self._latest_uploads:
            return self._latest_uploads[cache_key]

        # 2. Fallback: query Qdrant to find the newest point for this user in this collection
        try:
            from qdrant_client.http.models import Filter, FieldCondition, MatchValue
            client = self.vector_manager.get_client()
            
            # Map collection key to Qdrant collection name
            from rag.vector_store.vector_models import COLLECTIONS
            collection_name = COLLECTIONS[self.collection_key].name
            
            # Scroll points for this user in this collection
            records, _ = client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                ),
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            
            if not records:
                return None
                
            # Find the record with the most recent created_at timestamp
            latest_time = None
            latest_doc_id = None
            
            for record in records:
                payload = record.payload or {}
                # Match either document_id or source_id
                doc_id = payload.get("document_id") or payload.get("source_id")
                created_at_str = payload.get("created_at")
                
                if doc_id and created_at_str:
                    try:
                        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                        if latest_time is None or created_at > latest_time:
                            latest_time = created_at
                            latest_doc_id = doc_id
                    except Exception:
                        if latest_doc_id is None:
                            latest_doc_id = doc_id
                            
            if latest_doc_id:
                # Cache it in memory for next time
                self._latest_uploads[cache_key] = latest_doc_id
                return latest_doc_id
        except Exception as e:
            print(f"[{self.__class__.__name__}] Error fetching latest file from Qdrant: {e}", flush=True)
            
        return None

    # --------------------------------------------------
    # Convenience Methods
    # --------------------------------------------------

    def search_by_user(

        self,

        query: str,

        user_id: int,

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters={

                    "user_id": user_id

                }

            )

        )

    def search_by_source(

        self,

        query: str,

        source_id: str,

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                limit=limit,

                score_threshold=score_threshold,

                filters={

                    "source_id": source_id

                }

            )

        )

    def search_with_filters(

        self,

        query: str,

        filters: Dict[str, Any],

        limit: int = 5,

        score_threshold: Optional[float] = None

    ) -> List[SearchResult]:

        return (

            self.search(

                query=query,

                filters=filters,

                limit=limit,

                score_threshold=score_threshold

            )

        )