from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    LabelEncoder
)

from tools.ds_tools.target_detector import (
    TargetDetector
)

from tools.nlp_tools.nlp_feature_engineer import (
    NLPFeatureEngineer
)

from tools.nlp_tools.nlp_model_trainer import (
    NLPModelTrainer
)


from tools.nlp_tools.nlp_evaluator import (
    NLPEvaluator
)


class NLPAutoMLEngine:

    def run(
        self,
        df
    ):

        # ==================
        # Target Detection
        # ==================

        detector = (
            TargetDetector()
        )

        detection = (
            detector.detect(
                df
            )
        )

        target = (
            detection["target"]
        )

        # ==================
        # Text Column Detection
        # ==================

        import pandas as pd

        text_column = None

        for col in df.columns:

            if col == target:
                continue

            if (

                pd.api.types.is_object_dtype(
                    df[col]
                )

                or

                pd.api.types.is_string_dtype(
                    df[col]
                )

            ):

                text_column = col

                print(
                    f"\nTEXT COLUMN FOUND: {col}"
                )

                break

        if text_column is None:

            raise ValueError(
                "No text column found."
            )

        # ==================
        # Target Encoding
        # ==================

        encoder = (
            LabelEncoder()
        )

        df[target] = (
            encoder.fit_transform(
                df[target]
                .astype(str)
            )
        )

        # ==================
        # TF-IDF
        # ==================

        feature_engineer = (
            NLPFeatureEngineer()
        )

        processed = (
            feature_engineer.process(
                df,
                text_column,
                target
            )
        )

        X = processed["X"]
        y = processed["y"]

        # ==================
        # Split
        # ==================

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        # ==================
        # Train
        # ==================

        trainer = (
            NLPModelTrainer()
        )

        models = (
            trainer.train_models(
                X_train,
                y_train
            )
        )

        # ==================
        # Evaluate
        # ==================

        evaluator = (
            NLPEvaluator()
        )

        results = (
            evaluator.evaluate(
                models,
                X_test,
                y_test
            )
        )

        # ==================
        # Best Model
        # ==================

        best_model = max(

            results,

            key=lambda x:
            results[x][
                "Accuracy"
            ]

        )


        # ==================
        # Best Metrics
        # ==================

        accuracy = (

            results[
                best_model
            ][
                "Accuracy"
            ]

        )

        f1 = (

            results[
                best_model
            ][
                "F1"
            ]

        )

        return {

            "problem_type":
                "nlp_classification",

            "target":
                target,

            "text_column":
                text_column,

            "best_model":
                best_model,

            "leaderboard":
                results,

            "pipeline_type":
                "nlp",
                        
            "accuracy":
                accuracy,

            "f1":
                f1,

            "results":
                results
        }