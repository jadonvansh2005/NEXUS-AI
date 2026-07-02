from dataclasses import dataclass

from typing import Optional

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_constants import (
    SourceType,
    MemoryType,
    Permanence,
    ImportanceLevel
)


@dataclass
class SemanticMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Memory Information
    # --------------------------------------------------

    memory_id: Optional[str] = None

    memory_type: Optional[str] = None

    category: Optional[str] = None

    subcategory: Optional[str] = None

    # --------------------------------------------------
    # Semantic Properties
    # --------------------------------------------------

    permanence: str = (

        Permanence.LONG_TERM.value

    )

    confidence_score: float = 1.0

    importance_score: float = (

        ImportanceLevel.NORMAL.value

    )

    access_count: int = 0

    last_accessed_at: Optional[str] = None

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    related_memory_id: Optional[str] = None

    parent_memory_id: Optional[str] = None

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    def __post_init__(

        self

    ) -> None:

        if not self.source:

            self.source = (

                SourceType.SEMANTIC.value

            )

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def is_preference(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.PREFERENCE.value

        )

    def is_fact(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.FACT.value

        )

    def is_skill(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.SKILL.value

        )

    def is_goal(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.GOAL.value

        )

    def is_decision(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.DECISION.value

        )

    def is_profile(

        self

    ) -> bool:

        return (

            self.memory_type ==

            MemoryType.PROFILE.value

        )

    # --------------------------------------------------
    # Permanence
    # --------------------------------------------------

    def is_short_term(

        self

    ) -> bool:

        return (

            self.permanence ==

            Permanence.SHORT_TERM.value

        )

    def is_medium_term(

        self

    ) -> bool:

        return (

            self.permanence ==

            Permanence.MEDIUM_TERM.value

        )

    def is_long_term(

        self

    ) -> bool:

        return (

            self.permanence ==

            Permanence.LONG_TERM.value

        )

    def is_permanent(

        self

    ) -> bool:

        return (

            self.permanence ==

            Permanence.PERMANENT.value

        )

    # --------------------------------------------------
    # Memory Usage
    # --------------------------------------------------

    def increase_access_count(

        self

    ) -> None:

        self.access_count += 1

    def reset_access_count(

        self

    ) -> None:

        self.access_count = 0

    def has_parent(

        self

    ) -> bool:

        return (

            self.parent_memory_id

            is not None

        )

    def has_related_memory(

        self

    ) -> bool:

        return (

            self.related_memory_id

            is not None

        )