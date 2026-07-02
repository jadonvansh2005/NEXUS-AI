from typing import Any
from typing import Dict
from typing import Type

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

from rag.metadata.metadata_constants import (
    SourceType
)


_METADATA_REGISTRY: Dict[
    str,
    Type[BaseMetadata]
] = {

    SourceType.CONVERSATION.value:
        ConversationMetadata,

    SourceType.DOCUMENT.value:
        DocumentMetadata,

    SourceType.SEMANTIC.value:
        SemanticMetadata,

    SourceType.PROJECT.value:
        ProjectMetadata,

    SourceType.KNOWLEDGE.value:
        KnowledgeMetadata,

    SourceType.CODE.value:
        CodeMetadata,

}


class MetadataFactory:


    @staticmethod
    def create(

        source: str,

        **kwargs: Any

    ) -> BaseMetadata:

        metadata_class = (

            _METADATA_REGISTRY.get(

                source

            )

        )

        if metadata_class is None:

            raise ValueError(

                f"Unsupported metadata source: {source}"

            )

        return metadata_class(

            **kwargs

        )


    @staticmethod
    def register(

        source: str,

        metadata_class: Type[BaseMetadata]

    ) -> None:

        _METADATA_REGISTRY[

            source

        ] = metadata_class


    @staticmethod
    def conversation(

        **kwargs: Any

    ) -> ConversationMetadata:

        return ConversationMetadata(

            **kwargs

        )


    @staticmethod
    def document(

        **kwargs: Any

    ) -> DocumentMetadata:

        return DocumentMetadata(

            **kwargs

        )


    @staticmethod
    def semantic(

        **kwargs: Any

    ) -> SemanticMetadata:

        return SemanticMetadata(

            **kwargs

        )


    @staticmethod
    def project(

        **kwargs: Any

    ) -> ProjectMetadata:

        return ProjectMetadata(

            **kwargs

        )


    @staticmethod
    def knowledge(

        **kwargs: Any

    ) -> KnowledgeMetadata:

        return KnowledgeMetadata(

            **kwargs

        )


    @staticmethod
    def code(

        **kwargs: Any

    ) -> CodeMetadata:

        return CodeMetadata(

            **kwargs

        )


    @staticmethod
    def supported_sources(

        ) -> list[str]:

        return list(

            _METADATA_REGISTRY.keys()

        )