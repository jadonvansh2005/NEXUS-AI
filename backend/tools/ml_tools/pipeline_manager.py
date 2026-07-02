import os
import joblib


class PipelineManager:

    def __init__(self):

        self.model_dir = (
            "saved_models"
        )

    def save_pipeline(
        self,
        pipeline,
        model_name
    ):

        path = os.path.join(

            self.model_dir,

            f"{model_name}_pipeline.pkl"
        )

        joblib.dump(
            pipeline,
            path
        )

        return path

    def load_pipeline(
        self,
        model_name
    ):

        path = os.path.join(

            self.model_dir,

            f"{model_name}_pipeline.pkl"
        )

        return joblib.load(
            path
        )