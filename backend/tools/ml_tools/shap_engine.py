import shap
import pandas as pd
import numpy as np


class SHAPEngine:

    def explain_global(
        self,
        model,
        X
    ):

        try:

            explainer = shap.TreeExplainer(
                model
            )

            shap_values = (
                explainer.shap_values(
                    X
                )
            )

            if isinstance(
                shap_values,
                list
            ):
                shap_values = shap_values[0]

            importance = {}

            for i, col in enumerate(
                X.columns
            ):

                importance[col] = round(

                    float(

                        np.abs(
                            shap_values[:, i]
                        ).mean()

                    ),

                    4

                )

            return dict(

                sorted(

                    importance.items(),

                    key=lambda x: x[1],

                    reverse=True

                )

            )

        except Exception as e:

            return {
                "error": str(e)
            }

    def explain_local(
        self,
        model,
        X,
        row_index=0
    ):

        try:

            explainer = shap.TreeExplainer(
                model
            )

            shap_values = (
                explainer.shap_values(
                    X
                )
            )

            if isinstance(
                shap_values,
                list
            ):
                shap_values = shap_values[0]

            explanation = {}

            for i, col in enumerate(
                X.columns
            ):

                explanation[col] = round(

                    float(

                        shap_values[
                            row_index
                        ][i]

                    ),

                    4

                )

            return explanation

        except Exception as e:

            return {
                "error": str(e)
            }