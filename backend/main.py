import sys
import os

# Clean GCP environment credentials immediately on startup to prevent conflict with local API Key authentication
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("GOOGLE_API_KEY", None)
os.environ.pop("GOOGLE_OAUTH_TOKEN", None)

import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

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

import pandas as pd

from tools.ds_tools.target_detector import TargetDetector
from tools.ds_tools.dataset_type_detector import DatasetTypeDetector
from tools.nlp_tools.nlp_automl_engine import NLPAutoMLEngine

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

        df = pd.read_csv(file_path)

        target_detector = TargetDetector()

        target_info = target_detector.detect(df)

        dataset_detector = DatasetTypeDetector()

        dataset_info = dataset_detector.detect(
            df,
            target_info["target"],
        )

        if dataset_info["dataset_type"] == "structured":

            automl = AutoMLEngine()

            automl_result = automl.run(file_path)

        else:

            automl = NLPAutoMLEngine()

            automl_result = automl.run(

                df,

                dataset_info["text_columns"]

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

        model_charts = {}

        if (
            "results" in automl_result
            and
            "feature_scores" in automl_result
        ):
            model_charts = (
                model_visualizer.generate_all(
                    automl_result.get("results", {}),
                    automl_result.get("feature_scores", {}),
                    automl_result.get("model_importance", {}),
                    automl_result.get("problem_type", "classification")
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
                automl_result.get("problem_type"),

            "target":
                automl_result.get("target"),

            "best_model":
                automl_result.get("best_model"),

            "leaderboard":
                automl_result.get("leaderboard"),

            "feature_scores":
                automl_result.get("feature_scores", {}),

            "model_importance":
                automl_result.get("model_importance", {}),

            "saved_model":
                automl_result.get("saved_model_path"),

            "metadata":
                automl_result.get("metadata_path"),

            "pdf_report":
                pdf_path

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )