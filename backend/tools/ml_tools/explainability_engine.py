import pandas as pd


class ExplainabilityEngine:

    def explain(
        self,
        model,
        feature_names
    ):

        if hasattr(
            model,
            "feature_importances_"
        ):

            scores = {

                feature: int(importance)

                for feature, importance

                in zip(

                    feature_names,

                    model.feature_importances_

                )
            }

            scores = dict(

                sorted(

                    scores.items(),

                    key=lambda x: x[1],

                    reverse=True

                )

            )

            return scores

        return {}