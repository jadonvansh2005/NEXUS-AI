from rag.pipelines.base_pipeline import (
    BasePipeline
)

from rag.services.code_service import (
    CodeService
)


class CodePipeline(

    BasePipeline

):

    def __init__(

        self

    ):

        super().__init__(

            CodeService()

        )