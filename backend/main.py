from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

import os

from app.settings import settings
from api.router import api_router
from fastapi.middleware.cors import (
    CORSMiddleware
)

from tools.ds_tools.dataset_analyzer import (
    DatasetAnalyzer
)

from tools.ds_tools.visualization_generator import (
    VisualizationGenerator
)

from tools.ml_tools.automl_engine import (
    AutoMLEngine
)

from tools.ml_tools.model_visualizer import (
    ModelVisualizer
)

from api.routes.protected import (
    router as protected_router
)

from api.routes.conversations import (
    router as conversation_router
)

from api.routes.auth import (
    router as auth_router
)

from tools.report_tools.pdf_report_generator import (
    PDFReportGenerator
)

app = FastAPI(
    title="UPSS AutoML API"
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
        # "http://127.0.0.1:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)
app.include_router(api_router)

app.include_router(

    auth_router,

    prefix="/auth",

    tags=["Authentication"]

)

app.include_router(

    conversation_router,

    prefix="/conversations",

    tags=["Conversations"]

)

app.include_router(
    protected_router
)

@app.get("/")
def home():

    return {

        "status": "running",

        "project": "UPSS"

    }


@app.post("/datascience/run")

async def run_datascience_pipeline(

    file: UploadFile = File(...)

):

    try:

        # ====================
        # Save Dataset
        # ====================

        upload_dir = (
            "uploads/datasets"
        )

        os.makedirs(

            upload_dir,

            exist_ok=True

        )

        file_path = (

            f"{upload_dir}/{file.filename}"
        )

        with open(

            file_path,

            "wb"

        ) as f:

            f.write(

                await file.read()

            )

        # ====================
        # Dataset Analysis
        # ====================

        analyzer = (
            DatasetAnalyzer()
        )

        dataset_report = (
            analyzer.analyze(
                file_path
            )
        )

        # ====================
        # EDA Charts
        # ====================

        eda_generator = (
            VisualizationGenerator()
        )

        eda_charts = (
            eda_generator.generate(
                file_path
            )
        )

        # ====================
        # AutoML
        # ====================

        automl = (
            AutoMLEngine()
        )

        automl_result = (
            automl.run(
                file_path
            )
        )

        # ====================
        # Model Charts
        # ====================

        model_visualizer = (
            ModelVisualizer()
        )

        model_charts = (

            model_visualizer.generate_all(

                automl_result[
                    "results"
                ],

                automl_result[
                    "feature_scores"
                ],

                automl_result[
                    "model_importance"
                ],

                automl_result[
                    "problem_type"
                ]

            )

        )

        # ====================
        # PDF Report
        # ====================

        pdf_generator = (
            PDFReportGenerator()
        )

        pdf_path = (

            pdf_generator.generate(

                dataset_report,

                automl_result,

                eda_charts,

                model_charts

            )

        )

        # ====================
        # Response
        # ====================

        return {

            "success": True,

            "dataset_report":
                dataset_report,

            "problem_type":
                automl_result[
                    "problem_type"
                ],

            "target":
                automl_result[
                    "target"
                ],

            "best_model":
                automl_result[
                    "best_model"
                ],

            "leaderboard":
                automl_result[
                    "leaderboard"
                ],

            "feature_scores":
                automl_result[
                    "feature_scores"
                ],

            "model_importance":
                automl_result[
                    "model_importance"
                ],

            "saved_model":
                automl_result[
                    "saved_model_path"
                ],

            "metadata":
                automl_result[
                    "metadata_path"
                ],

            "pdf_report":
                pdf_path

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )