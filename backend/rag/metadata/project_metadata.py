from dataclasses import dataclass

from typing import Optional

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_constants import (
    SourceType,
    ProjectModule,
    ArchitectureLayer,
    ImportanceLevel
)


@dataclass
class ProjectMetadata(

    BaseMetadata

):

    # --------------------------------------------------
    # Project Information
    # --------------------------------------------------

    project_id: Optional[str] = None

    project_name: Optional[str] = None

    module: Optional[str] = None

    submodule: Optional[str] = None

    component: Optional[str] = None

    # --------------------------------------------------
    # Architecture
    # --------------------------------------------------

    architecture_layer: Optional[str] = None

    feature: Optional[str] = None

    workflow: Optional[str] = None

    design_pattern: Optional[str] = None

    # --------------------------------------------------
    # Development
    # --------------------------------------------------

    development_phase: Optional[str] = None

    milestone: Optional[str] = None

    version: Optional[str] = None

    # --------------------------------------------------
    # Repository
    # --------------------------------------------------

    repository: Optional[str] = None

    branch: Optional[str] = None

    commit_hash: Optional[str] = None


    # --------------------------------------------------
    # Chunk Information 
    # --------------------------------------------------

    page_number: Optional[int] = None

    chunk_index: Optional[int] = None

    total_chunks: Optional[int] = None

    # --------------------------------------------------
    # Source
    # --------------------------------------------------

    file_path: Optional[str] = None

    folder_path: Optional[str] = None

    line_start: Optional[int] = None

    line_end: Optional[int] = None

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    tags: Optional[list[str]] = None

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

                SourceType.PROJECT.value

            )

    # --------------------------------------------------
    # Module Helpers
    # --------------------------------------------------

    def is_memory_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.MEMORY.value

        )

    def is_rag_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.RAG.value

        )

    def is_agent_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.AGENT.value

        )

    def is_database_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.DATABASE.value

        )

    def is_backend_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.BACKEND.value

        )

    def is_frontend_module(

        self

    ) -> bool:

        return (

            self.module ==

            ProjectModule.FRONTEND.value

        )

    # --------------------------------------------------
    # Architecture Helpers
    # --------------------------------------------------

    def is_backend(

        self

    ) -> bool:

        return (

            self.architecture_layer ==

            ArchitectureLayer.BACKEND.value

        )

    def is_frontend(

        self

    ) -> bool:

        return (

            self.architecture_layer ==

            ArchitectureLayer.FRONTEND.value

        )

    def is_database(

        self

    ) -> bool:

        return (

            self.architecture_layer ==

            ArchitectureLayer.DATABASE.value

        )

    def is_ai(

        self

    ) -> bool:

        return (

            self.architecture_layer ==

            ArchitectureLayer.AI.value

        )

    def is_devops(

        self

    ) -> bool:

        return (

            self.architecture_layer ==

            ArchitectureLayer.DEVOPS.value

        )

    # --------------------------------------------------
    # Repository Helpers
    # --------------------------------------------------

    def has_file(

        self

    ) -> bool:

        return (

            self.file_path

            is not None

        )

    def has_commit(

        self

    ) -> bool:

        return (

            self.commit_hash

            is not None

        )

    def has_branch(

        self

    ) -> bool:

        return (

            self.branch

            is not None

        )

    def has_tags(

        self

    ) -> bool:

        return (

            self.tags is not None

            and

            len(

                self.tags

            ) > 0

        )