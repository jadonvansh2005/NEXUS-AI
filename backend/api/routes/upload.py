from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from tools.ds_tools.dataset_analyzer import (
    DatasetAnalyzer
)

from tools.ds_tools.dataset_insight_generator import (
    DatasetInsightGenerator
)

import os

router = APIRouter()
analyzer = DatasetAnalyzer()




@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...)
):

    upload_dir = (
        "uploads/datasets"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    report = analyzer.analyze(
        file_path
    )

    generator = (
        DatasetInsightGenerator()
    )

    insights = (
        generator.generate(
            report
        )
    )

    return {

        "message":
            "Analysis Complete",

        "file_path":
            file_path,

        "dataset_summary":
            {
                "rows":
                    report["rows"],

                "columns":
                    report["columns"],

                "missing_values":
                    report["missing_values"]
            },

        "ai_insights":
            insights
    }