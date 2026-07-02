import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    LabelEncoder
)

from tools.ds_tools.target_detector import (
    TargetDetector
)

from tools.ml_tools.model_trainer import (
    ModelTrainer
)

# from tools.ml_tools.nlp_detector import (
#     NLPDetector
# )

from tools.ml_tools.model_evaluator import (
    ModelEvaluator
)

from tools.ml_tools.model_manager import (
    ModelManager
)

from tools.ml_tools.model_selector import (
    ModelSelector
)

from tools.ml_tools.pipeline_manager import (
    PipelineManager
)

from tools.ml_tools.data_cleaner import (
    DataCleaner
)

# from tools.ml_tools.nlp_detector import (
#     NLPDetector
# )

from tools.ml_tools.feature_engineer import (
    FeatureEngineer
)

from tools.ml_tools.top_model_optimizer import (
    TopModelOptimizer
)

# from tools.nlp_tools.nlp_automl_engine import (
#     NLPAutoMLEngine
# )

from tools.ml_tools.explainability_engine import (
    ExplainabilityEngine
)



class AutoMLEngine:

    def run(
        self,
        file_path: str
    ):

        # ------------------
        # Load Dataset
        # ------------------

        df = pd.read_csv(
            file_path
        )

        # print("\n===== DATAFRAME INFO =====")
        # print(df.head())
        # print("\nDTYPES:")
        # print(df.dtypes)
        # print("=========================\n")

        # nlp_detector = (
        #     NLPDetector()
        # )

        # nlp_result = (
        #     nlp_detector.detect(
        #         df
        #     )
        # )

        # if nlp_result["is_nlp"]:

        #     print(
        #         "\nNLP Dataset Detected"
        #     )

        #     # from tools.nlp_tools.nlp_automl_engine import (
        #     #     NLPAutoMLEngine
        #     # )

        #     nlp_engine = (
        #         NLPAutoMLEngine()
        #     )

        #     return nlp_engine.run(
        #         df
        #     )

        # cleaner = (
        #     DataCleaner()
        # )

        # df = cleaner.clean(
        #     df
        # )

        # print("\n===== NLP DEBUG =====")
        # print(nlp_result)
        # print("=====================")

        # ------------------
        # Detect Target
        # ------------------

        detector = (
            TargetDetector()
        )

        # detection = (
        #     detector.detect(
        #         file_path
        #     )
        # )

        detection = (
            detector.detect(
                df
            )
        )

        target = (
            detection["target"]
        )

        explainer = (
            ExplainabilityEngine()
        )

        problem_type = (
            detection[
                "problem_type"
            ]
        )


        print("\n========== TARGET DEBUG ==========")

        print(
            "TARGET COLUMN:",
            target
        )

        print(
            "PROBLEM TYPE:",
            problem_type
        )

        print(
            "TARGET DTYPE:",
            df[target].dtype
        )

        print(
            "UNIQUE VALUES:",
            df[target].nunique()
        )

        print(
            "\nTARGET SAMPLE:"
        )

        print(
            df[target]
            .head(20)
            .tolist()
        )

        print(
            "==================================\n"
        )

        # ------------------
        # Encode Categories
        # ------------------

        engine = FeatureEngineer()

        processed = engine.process(
            df,
            target,
            problem_type
        )

        scaler = (
            processed["scaler"]
        )

        X = processed["X"]

        y = processed["y"]

        feature_scores = (
            processed["feature_scores"]
        )

        
        # ------------------
        # Split Data
        # ------------------

       

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        # ------------------
        # Train Models
        # ------------------

        trainer = (
            ModelTrainer()
        )

        models = (
            trainer.train_models(
                X_train,
                y_train,
                problem_type
            )
        )

        # ------------------
        # Evaluate Models
        # ------------------

        evaluator = (
            ModelEvaluator()
        )

        results = (
            evaluator.evaluate(
                models,
                X_test,
                y_test,
                problem_type
            )
        )

        if problem_type == "classification":

            leaderboard = sorted(

                results.items(),

                key=lambda x:
                x[1]["Accuracy"],

                reverse=True
            )

        else:

            leaderboard = sorted(

                results.items(),

                key=lambda x:
                x[1]["R2"],

                reverse=True
            )

        top_models = [

            model[0]

            for model

            in leaderboard[:3]

        ]

        optimizer = (
            TopModelOptimizer()
        )

        tuned_results = (

            optimizer.optimize(

                top_models,

                X_train,

                y_train,

                problem_type

            )

        )

        # ------------------
        # Select Best
        # ------------------

        selector = (
            ModelSelector()
        )

        print("\nRESULTS:")
        print(results)

        best_model = (
            selector.select_best(
                results,
                problem_type
            )
        )

        manager = (
            ModelManager()
        )

        saved_path = (
            manager.save_model(
                models[best_model],
                best_model
            )
        )


        pipeline = {

            "scaler":
                scaler,

            "columns":
                list(X.columns)
        }

        pipeline_manager = (
            PipelineManager()
        )

        pipeline_manager.save_pipeline(

            pipeline,

            best_model
        )

        metadata = {

            "feature_names":
                list(X.columns),

            "target":
                target,

            "problem_type":
                problem_type,

            "feature_scores":
                feature_scores
        }

        metadata_path = (
            manager.save_metadata(
                best_model,
                metadata
            )
        )

        model_importance = (
            explainer.explain(
                models[best_model],
                X.columns
            )
        )

        print(
            "\nSELECTED MODEL:",
            best_model
        )

        # best_model = (
        #     selector.select_best(
        #         results,
        #         problem_type
        #     )
        # )

        return {

            "problem_type":
                problem_type,

            "target":
                target,

            "results":
                results,

            "feature_scores":
                feature_scores,

            "best_model":
                best_model,

            "saved_model_path":
                saved_path,

            "leaderboard":
                leaderboard,

            "top_models":
                top_models,

            "tuned_results":
                tuned_results,
            
            "metadata_path":
                metadata_path,

            "model_importance":
                model_importance
        }