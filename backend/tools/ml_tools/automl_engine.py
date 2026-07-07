import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from tools.ds_tools.dataset_analyzer import (
    DatasetAnalyzer
)

from tools.ds_tools.dataset_insight_generator import (
    DatasetInsightGenerator
)

from tools.ds_tools.dataset_type_detector import (
    DatasetTypeDetector
)

from tools.ds_tools.target_detector import (
    TargetDetector
)

from tools.ml_tools.data_cleaner import (
    DataCleaner
)

from tools.ml_tools.feature_engineer import (
    FeatureEngineer
)

from tools.ml_tools.model_trainer import (
    ModelTrainer
)

from tools.ml_tools.model_evaluator import (
    ModelEvaluator
)

from tools.ml_tools.model_selector import (
    ModelSelector
)

from tools.ml_tools.model_manager import (
    ModelManager
)

from tools.ml_tools.pipeline_manager import (
    PipelineManager
)

from tools.ml_tools.top_model_optimizer import (
    TopModelOptimizer
)

from tools.ml_tools.explainability_engine import (
    ExplainabilityEngine
)

from tools.nlp_tools.nlp_automl_engine import (
    NLPAutoMLEngine
)


class AutoMLEngine:

    def run(
        self,
        file_path: str
    ):

        print("\n========== AUTOML START ==========\n")

        # =====================================
        # LOAD DATASET
        # =====================================

        df = pd.read_csv(
            file_path
        )

        print(
            f"Dataset Loaded : {len(df)} rows x {len(df.columns)} columns"
        )

        # =====================================
        # DATASET ANALYSIS
        # =====================================

        analyzer = DatasetAnalyzer()

        dataset_report = analyzer.analyze(
            file_path
        )

        print(
            "Dataset Analysis Completed."
        )

        # =====================================
        # DATASET INSIGHTS
        # =====================================

        insight_generator = (
            DatasetInsightGenerator()
        )

        dataset_insights = (
            insight_generator.generate(
                dataset_report
            )
        )

        print(
            "Dataset Insights Generated."
        )

        # =====================================
        # DATA CLEANING
        # =====================================

        cleaner = DataCleaner()

        df = cleaner.clean(
            df
        )

        print(
            "Data Cleaning Completed."
        )

        # =====================================
        # TARGET DETECTION
        # =====================================

        detector = TargetDetector()

        detection = detector.detect(
            df
        )

        target = detection[
            "target"
        ]

        problem_type = detection[
            "problem_type"
        ]

        # =====================================
        # DATASET TYPE DETECTION
        # =====================================

        dataset_detector = (
            DatasetTypeDetector()
        )

        dataset_type = (
            dataset_detector.detect(
                df,
                target
            )
        )

        print("\n========== DATASET TYPE ==========")

        print(dataset_type)

        print("==================================")

        # =====================================
        # NLP ROUTING
        # =====================================

        if dataset_type["is_nlp"]:

            print(
                "Routing Dataset To NLP Pipeline..."
            )

            nlp_engine = (
                NLPAutoMLEngine()
            )

            return nlp_engine.run(
                df,
                dataset_type["text_columns"]
            )

            nlp_result[
                "dataset_type"
            ] = dataset_type

            nlp_result[
                "dataset_report"
            ] = dataset_report

            nlp_result[
                "dataset_insights"
            ] = dataset_insights

            return nlp_result

        # =====================================
        # FEATURE ENGINEERING
        # =====================================

        feature_engineer = (
            FeatureEngineer()
        )

        processed = (
            feature_engineer.process(

                df,

                target,

                problem_type

            )
        )

        X = processed["X"]

        y = processed["y"]

        scaler = processed["scaler"]

        feature_scores = processed[
            "feature_scores"
        ]

        print(
            f"Total Features : {len(X.columns)}"
        )

        # =====================================
        # TRAIN TEST SPLIT
        # =====================================

        X_train, X_test, y_train, y_test = (

            train_test_split(

                X,

                y,

                test_size=0.20,

                random_state=42

            )

        )

        print(
            "Train/Test Split Completed."
        )

        # =====================================
        # TRAIN MODELS
        # =====================================

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

        print(
            f"{len(models)} Models Trained Successfully."
        )

        # =====================================
        # EVALUATE MODELS
        # =====================================

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

        print(
            "\n========== MODEL RESULTS =========="
        )

        print(results)

        print(
            "===================================\n"
        )

        # =====================================
        # LEADERBOARD
        # =====================================

        if problem_type == "classification":

            leaderboard = sorted(

                results.items(),

                key=lambda x: x[1]["Accuracy"],

                reverse=True

            )

        else:

            leaderboard = sorted(

                results.items(),

                key=lambda x: x[1]["R2"],

                reverse=True

            )

        print(
            "\n========== LEADERBOARD =========="
        )

        for rank, item in enumerate(

            leaderboard,

            start=1

        ):

            print(

                rank,

                item[0],

                item[1]

            )

        print(
            "=================================\n"
        )

        # =====================================
        # TOP 3 MODELS
        # =====================================

        top_models = [

            model_name

            for model_name, _

            in leaderboard[:3]

        ]

        # =====================================
        # HYPERPARAMETER OPTIMIZATION
        # =====================================

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

        # =====================================
        # BEST MODEL
        # =====================================

        selector = (
            ModelSelector()
        )

        best_model = (

            selector.select_best(

                results,

                problem_type

            )

        )

        print(
            f"\nBest Model : {best_model}"
        )

        # =====================================
        # SAVE MODEL
        # =====================================

        manager = (
            ModelManager()
        )

        saved_model_path = (

            manager.save_model(

                models[
                    best_model
                ],

                best_model

            )

        )

        # =====================================
        # SAVE PIPELINE
        # =====================================

        pipeline = {

            "scaler":
                scaler,

            "columns":
                list(
                    X.columns
                ),

            "target":
                target,

            "problem_type":
                problem_type,

            "dataset_type":
                dataset_type[
                    "dataset_type"
                ]

        }

        pipeline_manager = (
            PipelineManager()
        )

        pipeline_manager.save_pipeline(

            pipeline,

            best_model

        )

        # =====================================
        # SAVE METADATA
        # =====================================

        metadata = {

            "feature_names":
                list(
                    X.columns
                ),

            "target":
                target,

            "problem_type":
                problem_type,

            "dataset_type":
                dataset_type[
                    "dataset_type"
                ],

            "feature_scores":
                feature_scores

        }

        metadata_path = (

            manager.save_metadata(

                best_model,

                metadata

            )

        )

        # =====================================
        # EXPLAINABILITY
        # =====================================

        explainer = (
            ExplainabilityEngine()
        )

        model_importance = (

            explainer.explain(

                models[
                    best_model
                ],

                X.columns

            )

        )

        print(
            "\n========== AUTOML COMPLETED ==========\n"
        )

        return {

            "problem_type":
                problem_type,

            "dataset_type":
                dataset_type,

            "dataset_report":
                dataset_report,

            "dataset_insights":
                dataset_insights,

            "target":
                target,

            "results":
                results,

            "leaderboard":
                leaderboard,

            "best_model":
                best_model,

            "top_models":
                top_models,

            "tuned_results":
                tuned_results,

            "feature_scores":
                feature_scores,

            "model_importance":
                model_importance,

            "saved_model_path":
                saved_model_path,

            "metadata_path":
                metadata_path

        }