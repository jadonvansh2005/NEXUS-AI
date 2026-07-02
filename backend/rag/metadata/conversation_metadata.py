from dataclasses import dataclass

from typing import Optional

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_constants import (
    ConversationRole,
    SourceType,
    ImportanceLevel
)


@dataclass
class ConversationMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Conversation Information
    # --------------------------------------------------

    message_id: Optional[int] = None

    role: Optional[str] = None

    sequence_number: Optional[int] = None

    thread_id: Optional[str] = None

    # --------------------------------------------------
    # Conversation Retrieval
    # --------------------------------------------------

    chunk_index: Optional[int] = None

    total_chunks: Optional[int] = None

    previous_message_id: Optional[int] = None

    next_message_id: Optional[int] = None

    # --------------------------------------------------
    # Conversation Context
    # --------------------------------------------------

    session_name: Optional[str] = None

    domain: Optional[str] = None

    topic: Optional[str] = None

    # --------------------------------------------------
    # Retrieval Quality
    # --------------------------------------------------

    importance_score: float = (

        ImportanceLevel.NORMAL.value

    )

    confidence_score: float = 1.0

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    def __post_init__(

        self

    ) -> None:

        if not self.source:

            self.source = (

                SourceType.CONVERSATION.value

            )

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def is_user_message(

        self

    ) -> bool:

        return (

            self.role ==

            ConversationRole.USER.value

        )

    def is_assistant_message(

        self

    ) -> bool:

        return (

            self.role ==

            ConversationRole.ASSISTANT.value

        )

    def is_system_message(

        self

    ) -> bool:

        return (

            self.role ==

            ConversationRole.SYSTEM.value

        )

    def is_tool_message(

        self

    ) -> bool:

        return (

            self.role ==

            ConversationRole.TOOL.value

        )

    def has_previous(

        self

    ) -> bool:

        return (

            self.previous_message_id

            is not None

        )

    def has_next(

        self

    ) -> bool:

        return (

            self.next_message_id

            is not None

        )

    def is_chunked(

        self

    ) -> bool:

        return (

            self.chunk_index

            is not None

        )

    def is_first_chunk(

        self

    ) -> bool:

        return (

            self.chunk_index == 0

        )

    def is_last_chunk(

        self

    ) -> bool:

        if (

            self.chunk_index is None

            or

            self.total_chunks is None

        ):

            return False

        return (

            self.chunk_index ==

            self.total_chunks - 1

        )