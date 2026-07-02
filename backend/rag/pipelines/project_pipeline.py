from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.project_service import (
    ProjectService
)


class ProjectPipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            ProjectService()

        )