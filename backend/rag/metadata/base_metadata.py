from dataclasses import (
    dataclass,
    field,
    asdict
)
from datetime import datetime

from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class BaseMetadata:

    # --------------------------------------------------
    # Ownership
    # --------------------------------------------------

    user_id: Optional[int] = None

    project: Optional[str] = None

    conversation_id: Optional[int] = None

    # --------------------------------------------------
    # Source Information
    # --------------------------------------------------

    source: str = ""

    source_id: Optional[str] = None

    # --------------------------------------------------
    # Embedding Information
    # --------------------------------------------------

    embedding_model: str = ""

    embedding_dimension: Optional[int] = None

    # --------------------------------------------------
    # Versioning
    # --------------------------------------------------

    metadata_version: str = "1.0"

    # --------------------------------------------------
    # Extra Metadata
    # --------------------------------------------------

    extra: Dict[str, Any] = field(

        default_factory=dict

    )

    # --------------------------------------------------
    # Timestamp
    # --------------------------------------------------

    created_at: datetime = field(

        default_factory=datetime.utcnow

    )

    updated_at: Optional[datetime] = None

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def update_timestamp(

        self

    ) -> None:

        self.updated_at = (

            datetime.utcnow()

        )

    def add_extra(

        self,

        key: str,

        value: Any

    ) -> None:

        self.extra[

            key

        ] = value

    def get_extra(

        self,

        key: str,

        default: Any = None

    ) -> Any:

        return (

            self.extra.get(

                key,

                default

            )

        )

    def to_dict(

        self

    ) -> Dict[str, Any]:

        data = asdict(

            self

        )

        for key, value in data.items():

            if isinstance(

                value,

                datetime

            ):

                data[key] = (

                    value.isoformat()

                )

        return data