from sklearn.model_selection import (
    RandomizedSearchCV
)

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor
)

from xgboost import (
    XGBClassifier,
    XGBRegressor
)

from lightgbm import (
    LGBMClassifier,
    LGBMRegressor
)

from catboost import (
    CatBoostClassifier,
    CatBoostRegressor
)


class TopModelOptimizer:

    def optimize(
        self,
        model_names,
        X_train,
        y_train,
        problem_type
    ):

        results = {}

        for name in model_names:

            if problem_type == "classification":

                model, params = (
                    self._classification_config(
                        name
                    )
                )

                metric = "accuracy"

            else:

                model, params = (
                    self._regression_config(
                        name
                    )
                )

                metric = "r2"

            if model is None:

                continue

            search = RandomizedSearchCV(

                estimator=model,

                param_distributions=params,

                n_iter=5,

                cv=3,

                scoring=metric,

                random_state=42,

                n_jobs=-1

            )

            search.fit(
                X_train,
                y_train
            )

            results[name] = {

                "best_model":
                    search.best_estimator_,

                "best_params":
                    search.best_params_,

                "best_score":
                    float(
                        round(
                            search.best_score_,
                            4
                        )
                    )
            }

        return results
    
    def _classification_config(
        self,
        name
    ):

        configs = {

            "RandomForest": (

                RandomForestClassifier(),

                {
                    "n_estimators":
                        [100, 200, 300],

                    "max_depth":
                        [5, 10, 20]
                }
            ),

            "GradientBoosting": (

                GradientBoostingClassifier(),

                {
                    "n_estimators":
                        [100, 200],

                    "learning_rate":
                        [0.01, 0.05, 0.1]
                }
            ),

            "LightGBM": (

                LGBMClassifier(),

                {
                    "n_estimators":
                        [100, 200],

                    "max_depth":
                        [5, 10, 20]
                }
            ),

            "XGBoost": (

                XGBClassifier(),

                {
                    "n_estimators":
                        [100, 200],

                    "max_depth":
                        [3, 5, 10]
                }
            ),

            "CatBoost": (

                CatBoostClassifier(
                    verbose=0
                ),

                {
                    "depth":
                        [4, 6, 8],

                    "iterations":
                        [100, 200]
                }
            )
        }

        return configs.get(
            name,
            (None, None)
        )
    
    def _regression_config(
            self,
            name
        ):

            configs = {

                "RandomForest": (

                    RandomForestRegressor(),

                    {
                        "n_estimators":
                            [100, 200, 300],

                        "max_depth":
                            [5, 10, 20]
                    }
                ),

                "GradientBoosting": (

                    GradientBoostingRegressor(),

                    {
                        "n_estimators":
                            [100, 200],

                        "learning_rate":
                            [0.01, 0.05, 0.1]
                    }
                ),

                "LightGBM": (

                    LGBMRegressor(),

                    {
                        "n_estimators":
                            [100, 200],

                        "max_depth":
                            [5, 10, 20]
                    }
                ),

                "XGBoost": (

                    XGBRegressor(),

                    {
                        "n_estimators":
                            [100, 200],

                        "max_depth":
                            [3, 5, 10]
                    }
                ),

                "CatBoost": (

                    CatBoostRegressor(
                        verbose=0
                    ),

                    {
                        "depth":
                            [4, 6, 8],

                        "iterations":
                            [100, 200]
                    }
                )
            }

            return configs.get(
                name,
                (None, None)
            )
        