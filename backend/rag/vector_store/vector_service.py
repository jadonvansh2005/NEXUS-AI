from typing import List
from typing import Optional

from qdrant_client.http.models import (

    Distance,

    VectorParams,

    PointStruct,

    Filter,

    FieldCondition,

    MatchValue,

    UpdateStatus,

    PointIdsList

)

from rag.vector_store.vector_factory import (
    VectorFactory
)

from rag.vector_store.vector_schema import (

    VectorPoint,

    SearchResult,

    CollectionInfo

)

from rag.vector_store.vector_models import (

    COLLECTIONS,

    CollectionConfig

)

import uuid


class VectorService:

    def __init__(

        self

    ):

        self.client = (

            VectorFactory.get_client()

        )

    # ==========================================================
    # HEALTH CHECK
    # ==========================================================

    def health_check(

        self

    ) -> bool:

        try:

            self.client.get_collections()

            return True

        except Exception:

            return False

    # ==========================================================
    # COLLECTION MANAGEMENT
    # ==========================================================

    def collection_exists(

        self,

        collection_key: str

    ) -> bool:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        collections = (

            self.client.get_collections()

        )

        for collection in collections.collections:

            if (

                collection.name

                ==

                config.name

            ):

                return True

        return False

    def create_collection(

        self,

        collection_key: str

    ) -> bool:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        if (

            self.collection_exists(

                collection_key

            )

        ):

            return True

        self.client.create_collection(

            collection_name=config.name,

            vectors_config=VectorParams(

                size=config.vector_size,

                distance=Distance.COSINE

            )

        )

        return True

    def recreate_collection(

        self,

        collection_key: str

    ) -> bool:

        if (

            self.collection_exists(

                collection_key

            )

        ):

            self.delete_collection(

                collection_key

            )

        return (

            self.create_collection(

                collection_key

            )

        )

    def delete_collection(

        self,

        collection_key: str

    ) -> bool:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        if not (

            self.collection_exists(

                collection_key

            )

        ):

            return False

        self.client.delete_collection(

            collection_name=config.name

        )

        return True

    def list_collections(

        self

    ) -> List[str]:

        collections = (

            self.client.get_collections()

        )

        result = []

        for collection in collections.collections:

            result.append(

                collection.name

            )

        return result

    # ==========================================================
    # COLLECTION INFORMATION
    # ==========================================================

    def collection_info(

        self,

        collection_key: str

    ) -> CollectionInfo:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        info = (

            self.client.get_collection(

                config.name

            )

        )

        return CollectionInfo(

            collection_name=config.name,

            vector_size=config.vector_size,

            distance_metric=config.distance,

            points_count=info.points_count

        )

    def count_vectors(

        self,

        collection_key: str

    ) -> int:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        info = (

            self.client.get_collection(

                config.name

            )

        )

        return (

            info.points_count

        )
    

    # ==========================================================
    # VECTOR INSERTION
    # ==========================================================



    def insert_vector(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        config = (

            self._validate_collection(

                collection_key

            )

        )

        self._ensure_collection(

            collection_key

        )

        point_id = (

            point.id

            if point.id

            else

            str(

                uuid.uuid4()

            )

        )

        qdrant_point = (

            PointStruct(

                id=point_id,

                vector=point.embedding,

                payload=point.payload

            )

        )

        self.client.upsert(

            collection_name=config.name,

            wait=True,

            points=[

                qdrant_point

            ]

        )

        return True

    def insert_batch(

        self,

        collection_key: str,

        points: List[

            VectorPoint

        ]

    ) -> bool:

        config = (

            self._validate_collection(

                collection_key

            )

        )

        self._ensure_collection(

            collection_key

        )

        batch = []

        for point in points:

            point_id = (

                point.id

                if point.id

                else

                str(

                    uuid.uuid4()

                )

            )

            batch.append(

                PointStruct(

                    id=point_id,

                    vector=point.embedding,

                    payload=point.payload

                )

            )

        self.client.upsert(

            collection_name=config.name,

            wait=True,

            points=batch

        )

        return True

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_vector(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        return (

            self.insert_vector(

                collection_key,

                point

            )

        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_vector(

        self,

        collection_key: str,

        point_id: str

    ) -> bool:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        self.client.delete(

            collection_name=config.name,

            points_selector=PointIdsList(

                points=[

                    point_id

                ]

            ),

            wait=True

        )

        return True

    # ==========================================================
    # CLEAR COLLECTION
    # ==========================================================

    def clear_collection(

        self,

        collection_key: str

    ) -> bool:

        self.recreate_collection(

            collection_key

        )

        return True

    # ==========================================================
    # GET VECTOR
    # ==========================================================

    def get_vector(

        self,

        collection_key: str,

        point_id: str

    ) -> Optional[

        VectorPoint

    ]:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        result = (

            self.client.retrieve(

                collection_name=config.name,

                ids=[

                    point_id

                ]

            )

        )

        if not result:

            return None

        point = result[0]

        return VectorPoint(

            id=str(

                point.id

            ),

            embedding=point.vector,

            payload=point.payload

        )
    

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(

        self,

        collection_key: str,

        query_vector: List[float],

        limit: int = 5

    ) -> List[SearchResult]:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        results = (

            self.client.query_points(

                collection_name=config.name,

                query=query_vector,

                limit=limit

            ).points

        )

        search_results = []

        for result in results:

            search_results.append(

                SearchResult(

                    id=str(

                        result.id

                    ),

                    score=result.score,

                    payload=result.payload

                )

            )

        return search_results

    # ==========================================================
    # SEARCH WITH FILTERS
    # ==========================================================

    def search_by_filter(

        self,

        collection_key: str,

        query_vector: List[float],

        filters: dict,

        limit: int = 5

    ) -> List[SearchResult]:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        conditions = []

        for key, value in filters.items():

            conditions.append(

                FieldCondition(

                    key=key,

                    match=MatchValue(

                        value=value

                    )

                )

            )

        results = (

            self.client.query_points(

                collection_name=config.name,

                query=query_vector,

                query_filter=Filter(

                    must=conditions

                ),

                limit=limit

            ).points

        )

        search_results = []

        for result in results:

            search_results.append(

                SearchResult(

                    id=str(

                        result.id

                    ),

                    score=result.score,

                    payload=result.payload

                )

            )

        return search_results

    # ==========================================================
    # SEARCH BY IDS
    # ==========================================================

    def search_by_ids(

        self,

        collection_key: str,

        ids: List[str]

    ) -> List[VectorPoint]:

        config = (

            COLLECTIONS[

                collection_key

            ]

        )

        results = (

            self.client.retrieve(

                collection_name=config.name,

                ids=ids

            )

        )

        vectors = []

        for point in results:

            vectors.append(

                VectorPoint(

                    id=str(

                        point.id

                    ),

                    embedding=point.vector,

                    payload=point.payload

                )

            )

        return vectors

    # ==========================================================
    # UPSERT WITH AUTO UUID
    # ==========================================================

    def upsert_vector(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        import uuid

        if (

            point.id is None

            or

            point.id == ""

        ):

            point.id = (

                str(

                    uuid.uuid4()

                )

            )

        return (

            self.insert_vector(

                collection_key,

                point

            )

        )
    

    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _to_search_results(

        self,

        results

    ) -> List[SearchResult]:

        search_results = []

        for result in results:

            search_results.append(

                SearchResult(

                    id=str(

                        result.id

                    ),

                    score=result.score,

                    payload=result.payload

                )

            )

        return search_results

    def _to_vector_points(

        self,

        points

    ) -> List[VectorPoint]:

        vectors = []

        for point in points:

            vectors.append(

                VectorPoint(

                    id=str(

                        point.id

                    ),

                    embedding=point.vector,

                    payload=point.payload

                )

            )

        return vectors

    def _validate_collection(

        self,

        collection_key: str

    ) -> CollectionConfig:

        if (

            collection_key

            not in

            COLLECTIONS

        ):

            raise ValueError(

                f"Unknown collection: {collection_key}"

            )

        return (

            COLLECTIONS[

                collection_key

            ]

        )

    def _ensure_collection(

        self,

        collection_key: str

    ):

        if not (

            self.collection_exists(

                collection_key

            )

        ):

            self.create_collection(

                collection_key

            )

    # ==========================================================
    # INTERNAL VALIDATION
    # ==========================================================

    def validate_embedding_dimension(

        self,

        collection_key: str,

        embedding: List[float]

    ) -> bool:

        config = (

            self._validate_collection(

                collection_key

            )

        )

        return (

            len(

                embedding

            )

            ==

            config.vector_size

        )

    def validate_point(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        if (

            not self.validate_embedding_dimension(

                collection_key,

                point.embedding

            )

        ):

            return False

        if (

            point.payload

            is None

        ):

            return False

        return True

    # ==========================================================
    # CLIENT ACCESS
    # ==========================================================

    def get_client(

        self

    ):

        return (

            self.client

        )

    # ==========================================================
    # CACHE PLACEHOLDER
    # ==========================================================

    def flush(

        self

    ):

        """
        Reserved for future cache synchronization.
        """

        return True
    

    # ==========================================================
    # SAFE WRAPPERS
    # ==========================================================

    def safe_insert(

        self,

        collection_key: str,

        point: VectorPoint

    ) -> bool:

        try:

            if not self.validate_point(

                collection_key,

                point

            ):

                return False

            self._ensure_collection(

                collection_key

            )

            return self.upsert_vector(

                collection_key,

                point

            )

        except Exception as error:

            print(

                f"[VectorService] Insert Error: {error}"

            )

            return False

    def safe_batch_insert(

        self,

        collection_key: str,

        points: List[VectorPoint]

    ) -> bool:

        try:

            self._ensure_collection(

                collection_key

            )

            valid_points = []

            for point in points:

                if self.validate_point(

                    collection_key,

                    point

                ):

                    valid_points.append(

                        point

                    )

            if not valid_points:

                return False

            return self.insert_batch(

                collection_key,

                valid_points

            )

        except Exception as error:

            print(

                f"[VectorService] Batch Insert Error: {error}"

            )

            return False

    def safe_search(

        self,

        collection_key: str,

        query_vector: List[float],

        limit: int = 5

    ) -> List[SearchResult]:

        try:

            if not self.collection_exists(

                collection_key

            ):

                return []

            return self.search(

                collection_key,

                query_vector,

                limit

            )

        except Exception as error:

            print(

                f"[VectorService] Search Error: {error}"

            )

            return []

    def safe_delete(

        self,

        collection_key: str,

        point_id: str

    ) -> bool:

        try:

            return self.delete_vector(

                collection_key,

                point_id

            )

        except Exception as error:

            print(

                f"[VectorService] Delete Error: {error}"

            )

            return False

    def ping(

        self

    ) -> bool:

        return self.health_check()