import os

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns


class ModelVisualizer:

    # ==========================
    # MODEL LEADERBOARD
    # ==========================

    def generate_leaderboard_chart(

        self,

        results,

        problem_type

    ):

        output_dir = (
            "uploads/reports/model_charts"
        )

        os.makedirs(

            output_dir,

            exist_ok=True

        )

        if problem_type == "classification":

            metric = "Accuracy"

        else:

            metric = "R2"

        models = []

        scores = []

        for model_name, metrics in results.items():

            models.append(
                model_name
            )

            scores.append(
                metrics[metric]
            )

        leaderboard = pd.DataFrame({

            "Model":
                models,

            metric:
                scores

        })

        leaderboard = leaderboard.sort_values(

            metric,

            ascending=False

        )

        plt.figure(
            figsize=(10, 6)
        )

        sns.barplot(

            data=leaderboard,

            x=metric,

            y="Model"

        )

        plt.title(
            "Model Leaderboard"
        )

        plt.tight_layout()

        chart_path = (

            f"{output_dir}/leaderboard.png"

        )

        plt.savefig(
            chart_path
        )

        plt.close()

        return chart_path

    # ==========================
    # FEATURE IMPORTANCE
    # ==========================

    def generate_feature_importance_chart(

        self,

        feature_scores

    ):

        output_dir = (
            "uploads/reports/model_charts"
        )

        os.makedirs(

            output_dir,

            exist_ok=True

        )

        data = pd.DataFrame({

            "Feature":
                list(
                    feature_scores.keys()
                ),

            "Score":
                list(
                    feature_scores.values()
                )

        })

        data = data.sort_values(

            "Score",

            ascending=False

        ).head(20)

        plt.figure(
            figsize=(10, 8)
        )

        sns.barplot(

            data=data,

            x="Score",

            y="Feature"

        )

        plt.title(
            "Feature Importance"
        )

        plt.tight_layout()

        chart_path = (

            f"{output_dir}/feature_importance.png"

        )

        plt.savefig(
            chart_path
        )

        plt.close()

        return chart_path

    # ==========================
    # MODEL IMPORTANCE
    # ==========================

    def generate_model_importance_chart(

        self,

        model_importance

    ):

        if not model_importance:
            return ""

        output_dir = (
            "uploads/reports/model_charts"
        )

        os.makedirs(

            output_dir,

            exist_ok=True

        )

        data = pd.DataFrame({

            "Feature":
                list(
                    model_importance.keys()
                ),

            "Score":
                list(
                    model_importance.values()
                )

        })

        data = data.sort_values(

            "Score",

            ascending=False

        ).head(20)

        plt.figure(
            figsize=(10, 8)
        )

        sns.barplot(

            data=data,

            x="Score",

            y="Feature"

        )

        plt.title(
            "Model Importance"
        )

        plt.tight_layout()

        chart_path = (

            f"{output_dir}/model_importance.png"

        )

        plt.savefig(
            chart_path
        )

        plt.close()

        return chart_path

    # ==========================
    # GENERATE ALL CHARTS
    # ==========================

    def generate_all(

        self,

        results,

        feature_scores,

        model_importance,

        problem_type

    ):

        charts = {}

        charts[
            "leaderboard"
        ] = self.generate_leaderboard_chart(

            results,

            problem_type

        )

        charts[
            "feature_importance"
        ] = self.generate_feature_importance_chart(

            feature_scores

        )

        charts[
            "model_importance"
        ] = self.generate_model_importance_chart(

            model_importance

        )

        return charts