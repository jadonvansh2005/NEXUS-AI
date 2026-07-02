import pandas as pd

from tools.ml_tools.model_manager import (
    ModelManager
)

from tools.ml_tools.prediction_preprocessor import (
    PredictionPreprocessor
)


class PredictionEngine:

    def predict(
        self,
        model_name,
        data
    ):

        manager = (
            ModelManager()
        )

        model = manager.load_model(
            model_name
        )

        metadata = (
            manager.load_metadata(
                model_name
            )
        )

        df = pd.DataFrame(
            data
        )

        processor = (
            PredictionPreprocessor()
        )

        df = processor.prepare(
            df,
            metadata
        )

        predictions = (
            model.predict(df)
        )

        return (
            predictions.tolist()
        )