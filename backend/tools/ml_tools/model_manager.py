import os
import joblib


class ModelManager:

    def __init__(self):

        self.model_dir = "saved_models"

        os.makedirs(
            self.model_dir,
            exist_ok=True
        )

    def save_model(
        self,
        model,
        model_name
    ):

        path = os.path.join(
            self.model_dir,
            f"{model_name}.pkl"
        )

        joblib.dump(
            model,
            path
        )

        return path

    def load_model(
        self,
        model_name
    ):

        path = os.path.join(
            self.model_dir,
            f"{model_name}.pkl"
        )

        return joblib.load(
            path
        )

    def list_models(
        self
    ):

        return [

            file

            for file in os.listdir(
                self.model_dir
            )

            if file.endswith(
                ".pkl"
            )

        ]

    def delete_model(
        self,
        model_name
    ):

        path = os.path.join(
            self.model_dir,
            f"{model_name}.pkl"
        )

        if os.path.exists(path):

            os.remove(path)

            return True

        return False
    
    def save_metadata(
        self,
        model_name,
        metadata
    ):

        path = os.path.join(
            self.model_dir,
            f"{model_name}_metadata.pkl"
        )

        joblib.dump(
            metadata,
            path
        )

        return path
    

    def load_metadata(
        self,
        model_name
    ):

        path = os.path.join(
            self.model_dir,
            f"{model_name}_metadata.pkl"
        )

        return joblib.load(
            path
        )