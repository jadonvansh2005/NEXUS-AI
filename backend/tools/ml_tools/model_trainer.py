from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.tree import (
    DecisionTreeRegressor,
    DecisionTreeClassifier
)

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from xgboost import (
    XGBRegressor,
    XGBClassifier
)

from lightgbm import (
    LGBMRegressor,
    LGBMClassifier
)

from catboost import (
    CatBoostRegressor,
    CatBoostClassifier
)

from sklearn.ensemble import (
    AdaBoostRegressor,
    AdaBoostClassifier,

    GradientBoostingRegressor,
    GradientBoostingClassifier,

    ExtraTreesRegressor,
    ExtraTreesClassifier
)

from sklearn.svm import (
    SVR,
    SVC
)

from sklearn.neighbors import (
    KNeighborsRegressor,
    KNeighborsClassifier
)


class ModelTrainer:

    def train_models(
        self,
        X_train,
        y_train,
        problem_type
    ):

        models = {}

        if problem_type == "regression":

            models = {

                
                "LinearRegression":
                    LinearRegression(),

                "DecisionTree":
                    DecisionTreeRegressor(),

                "RandomForest":
                    RandomForestRegressor(
                        n_estimators=100,
                        random_state=42
                    ),

                "GradientBoosting":
                    GradientBoostingRegressor(),

                "AdaBoost":
                    AdaBoostRegressor(),

                "ExtraTrees":
                    ExtraTreesRegressor(),

                "XGBoost":
                    XGBRegressor(),

                "LightGBM":
                    LGBMRegressor(),

                "CatBoost":
                    CatBoostRegressor(
                        verbose=False
                    ),

                "SVR":
                    SVR(),

                "KNN":
                    KNeighborsRegressor()
            }
            

        else:

            models = {

                "LogisticRegression":
                    LogisticRegression(
                        max_iter=1000
                    ),

                "DecisionTree":
                    DecisionTreeClassifier(),

                "RandomForest":
                    RandomForestClassifier(
                        n_estimators=100,
                        random_state=42
                    ),

                "GradientBoosting":
                    GradientBoostingClassifier(),

                "AdaBoost":
                    AdaBoostClassifier(),

                "ExtraTrees":
                    ExtraTreesClassifier(),

                "XGBoost":
                    XGBClassifier(),

                "LightGBM":
                    LGBMClassifier(),

                "CatBoost":
                    CatBoostClassifier(
                        verbose=False
                    ),

                "SVC":
                    SVC(),

                "KNN":
                    KNeighborsClassifier()
            }

        trained_models = {}

        for name, model in models.items():

            model.fit(
                X_train,
                y_train
            )

            trained_models[
                name
            ] = model

        return trained_models