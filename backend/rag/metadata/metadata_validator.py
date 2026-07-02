from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.conversation_metadata import (
    ConversationMetadata
)

from rag.metadata.document_metadata import (
    DocumentMetadata
)

from rag.metadata.semantic_metadata import (
    SemanticMetadata
)

from rag.metadata.project_metadata import (
    ProjectMetadata
)

from rag.metadata.knowledge_metadata import (
    KnowledgeMetadata
)

from rag.metadata.code_metadata import (
    CodeMetadata
)


class MetadataValidator:


    @staticmethod
    def validate(

        metadata: BaseMetadata

    ) -> None:

        if metadata is None:

            raise ValueError(

                "Metadata cannot be None."

            )

        if not metadata.source:

            raise ValueError(

                "Metadata source is required."

            )

        if not metadata.embedding_model:

            raise ValueError(

                "Embedding model is required."

            )

        MetadataValidator._validate_type(

            metadata

        )


    @staticmethod
    def _validate_type(

        metadata: BaseMetadata

    ) -> None:

        if isinstance(

            metadata,

            ConversationMetadata

        ):

            MetadataValidator._validate_conversation(

                metadata

            )

            return


        if isinstance(

            metadata,

            DocumentMetadata

        ):

            MetadataValidator._validate_document(

                metadata

            )

            return


        if isinstance(

            metadata,

            SemanticMetadata

        ):

            MetadataValidator._validate_semantic(

                metadata

            )

            return


        if isinstance(

            metadata,

            ProjectMetadata

        ):

            MetadataValidator._validate_project(

                metadata

            )

            return


        if isinstance(

            metadata,

            KnowledgeMetadata

        ):

            MetadataValidator._validate_knowledge(

                metadata

            )

            return


        if isinstance(

            metadata,

            CodeMetadata

        ):

            MetadataValidator._validate_code(

                metadata

            )

            return


    @staticmethod
    def _validate_conversation(

        metadata: ConversationMetadata

    ) -> None:

        if metadata.role is None:

            raise ValueError(

                "Conversation role is required."

            )


    @staticmethod
    def _validate_document(

        metadata: DocumentMetadata

    ) -> None:

        if metadata.document_name is None:

            raise ValueError(

                "Document name is required."

            )


    @staticmethod
    def _validate_semantic(

        metadata: SemanticMetadata

    ) -> None:

        if metadata.memory_type is None:

            raise ValueError(

                "Memory type is required."

            )


    @staticmethod
    def _validate_project(

        metadata: ProjectMetadata

    ) -> None:

        if metadata.project_name is None:

            raise ValueError(

                "Project name is required."

            )


    @staticmethod
    def _validate_knowledge(

        metadata: KnowledgeMetadata

    ) -> None:

        if metadata.document_name is None:

            raise ValueError(

                "Knowledge document name is required."

            )


    @staticmethod
    def _validate_code(

        metadata: CodeMetadata

    ) -> None:

        if metadata.file_name is None:

            raise ValueError(

                "Code file name is required."

            )