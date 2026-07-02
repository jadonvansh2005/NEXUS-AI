from typing import List
from typing import Dict
from typing import Any
from typing import Optional

from rag.vector_store.vector_service import (
    VectorService
)

from rag.vector_store.vector_schema import (
    VectorPoint,
    SearchResult,
    CollectionInfo
)


class VectorManager:

    def __init__(

        self

    ):

        self.service = (

            VectorService()

        )

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health_check(

        self

    ) -> bool:

        return (

            self.service.health_check()

        )

    # ==========================================================
    # COLLECTIONS
    # ==========================================================

    def create_collection(

        self,

        collection_key: str

    ) -> bool:

        return (

            self.service.create_collection(

                collection_key

            )

        )

    def recreate_collection(

        self,

        collection_key: str

    ) -> bool:

        return (

            self.service.recreate_collection(

                collection_key

            )

        )

    def delete_collection(

        self,

        collection_key: str

    ) -> bool:

        return (

            self.service.delete_collection(

                collection_key

            )

        )

    def collection_exists(

        self,

        collection_key: str

    ) -> bool:

        return (

            self.service.collection_exists(

                collection_key

            )

        )

    def list_collections(

        self

    ) -> List[str]:

        return (

            self.service.list_collections()

        )

    def collection_info(

        self,

        collection_key: str

    ) -> CollectionInfo:

        return (

            self.service.collection_info(

                collection_key

            )

        )

    def count_vectors(

        self,

        collection_key: str

    ) -> int:

        return (

            self.service.count_vectors(

                collection_key

            )

        )

    # ==========================================================
    # INSERT
    # ==========================================================

    def insert(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        return (

            self.service.safe_insert(

                collection_key,

                point

            )

        )

    def insert_batch(

        self,

        collection_key: str,

        points: List[VectorPoint]

    ) -> bool:

        return (

            self.service.safe_batch_insert(

                collection_key,

                points

            )

        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        return (

            self.service.update_vector(

                collection_key,

                point

            )

        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(

        self,

        collection_key: str,

        point_id: str

    ) -> bool:

        return (

            self.service.safe_delete(

                collection_key,

                point_id

            )

        )

    def clear_collection(

        self,

        collection_key: str

    ) -> bool:

        return (

            self.service.clear_collection(

                collection_key

            )

        )

    # ==========================================================
    # GET
    # ==========================================================

    def get(

        self,

        collection_key: str,

        point_id: str

    ) -> Optional[VectorPoint]:

        return (

            self.service.get_vector(

                collection_key,

                point_id

            )

        )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(

        self,

        collection_key: str,

        query_vector: List[float],

        limit: int = 5,

        score_threshold: Optional[float] = None,

        filters: Optional[Dict[str, Any]] = None

    ) -> List[SearchResult]:

        if filters:

            results = (

                self.service.search_by_filter(

                    collection_key,

                    query_vector,

                    filters,

                    limit

                )

            )

        else:

            results = (

                self.service.safe_search(

                    collection_key,

                    query_vector,

                    limit

                )

            )

        if score_threshold is not None:

            results = [

                result

                for result in results

                if result.score >= score_threshold

            ]

        return results
    
    def search_by_filter(

        self,

        collection_key: str,

        query_vector: List[float],

        filters: Dict[str, Any],

        limit: int = 5

    ) -> List[SearchResult]:

        return (

            self.service.search_by_filter(

                collection_key,

                query_vector,

                filters,

                limit

            )

        )

    def search_by_ids(

        self,

        collection_key: str,

        ids: List[str]

    ) -> List[VectorPoint]:

        return (

            self.service.search_by_ids(

                collection_key,

                ids

            )

        )

    # ==========================================================
    # CLIENT
    # ==========================================================

    def get_client(

        self

    ):

        return (

            self.service.get_client()

        )