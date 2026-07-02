from sklearn.model_selection import (
    RandomizedSearchCV
)

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)


class HyperparameterOptimizer:

    def optimize(
        self,
        X_train,
        y_train,
        problem_type
    ):

        if problem_type == "regression":

            model = (
                RandomForestRegressor(
                    random_state=42
                )
            )

            params = {

                "n_estimators":
                    [100, 200, 300],

                "max_depth":
                    [None, 5, 10, 20],

                "min_samples_split":
                    [2, 5, 10]
            }

            metric = "r2"

        else:

            model = (
                RandomForestClassifier(
                    random_state=42
                )
            )

            params = {

                "n_estimators":
                    [100, 200, 300],

                "max_depth":
                    [None, 5, 10, 20],

                "min_samples_split":
                    [2, 5, 10]
            }

            metric = "accuracy"

        search = RandomizedSearchCV(

            estimator=model,

            param_distributions=params,

            n_iter=10,

            cv=3,

            scoring=metric,

            random_state=42,

            n_jobs=-1
        )

        search.fit(
            X_train,
            y_train
        )

        return {

            "best_model":
                search.best_estimator_,

            "best_params":
                search.best_params_,

            "best_score":
                round(
                    search.best_score_,
                    4
                )
        }