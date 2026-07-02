from dataclasses import dataclass

from typing import Dict
from typing import Any
from typing import List
from typing import Optional


@dataclass
class VectorPoint:

    id: Optional[str] = None

    embedding: Optional[List[float]] = None

    payload: Optional[Dict[str, Any]] = None


@dataclass
class SearchResult:

    id: str

    score: float

    payload: Dict[str, Any]



@dataclass
class CollectionInfo:

    collection_name: str

    vector_size: int

    distance_metric: str

    points_count: Optional[int] = None