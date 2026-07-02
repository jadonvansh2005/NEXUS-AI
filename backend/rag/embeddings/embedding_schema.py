from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Optional
from typing import Dict
from typing import Any


@dataclass
class EmbeddingResult:

    text: str

    embedding: List[float]

    model_name: str

    dimension: int

    source_type: str

    source_id: Optional[str]

    user_id: Optional[int]

    metadata: Dict[str, Any]

    created_at: datetime