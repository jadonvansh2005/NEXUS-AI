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

        print("\n========== HYPERPARAMETER OPTIMIZATION ==========\n")

        for name in model_names:

            if problem_type == "classification":

                model, params = self._classification_config(
                    name
                )

                metric = "accuracy"

            else:

                model, params = self._regression_config(
                    name
                )

                metric = "r2"

            if model is None:

                print(f"Skipping {name} (No Config Found)")
                continue

            try:

                print(f"Optimizing {name} ...")

                search = RandomizedSearchCV(

                    estimator=model,

                    param_distributions=params,

                    n_iter=3,

                    cv=2,

                    scoring=metric,

                    random_state=42,

                    n_jobs=1,

                    error_score="raise"

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

                print(f"{name} Optimization Completed")

            except Exception as e:

                print(f"{name} Optimization Failed")

                print(e)

                continue

        print("\n===============================================\n")

        return results

    def _classification_config(
        self,
        name
    ):

        configs = {

            "RandomForest": (

                RandomForestClassifier(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200, 300],

                    "max_depth":
                        [5, 10, 20],

                    "min_samples_split":
                        [2, 5]

                }

            ),

            "GradientBoosting": (

                GradientBoostingClassifier(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200],

                    "learning_rate":
                        [0.01, 0.05, 0.1]

                }

            ),

            "ExtraTrees": (

                ExtraTreesClassifier(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200],

                    "max_depth":
                        [None, 10, 20]

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
                    verbose=False
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

                RandomForestRegressor(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200, 300],

                    "max_depth":
                        [5, 10, 20],

                    "min_samples_split":
                        [2, 5]

                }

            ),

            "GradientBoosting": (

                GradientBoostingRegressor(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200],

                    "learning_rate":
                        [0.01, 0.05, 0.1]

                }

            ),

            "ExtraTrees": (

                ExtraTreesRegressor(
                    random_state=42
                ),

                {

                    "n_estimators":
                        [100, 200],

                    "max_depth":
                        [None, 10, 20]

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
                    verbose=False
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