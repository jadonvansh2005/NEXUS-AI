from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
    
    
)


class ModelEvaluator:

    def evaluate(
        self,
        models,
        X_test,
        y_test,
        problem_type
    ):

        results = {}

        for name, model in models.items():

            predictions = model.predict(
                X_test
            )

            if problem_type == "regression":

                results[name] = {

                    "R2":
                        round(
                            r2_score(
                                y_test,
                                predictions
                            ),
                            4
                        ),

                    "MAE":
                        round(
                            mean_absolute_error(
                                y_test,
                                predictions
                            ),
                            4
                        ),

                    "RMSE":
                        round(
                            mean_squared_error(
                                y_test,
                                predictions
                            ) ** 0.5,
                            4
                        )
                }

            else:

                results[name] = {

                    "Accuracy":
                        round(
                            accuracy_score(
                                y_test,
                                predictions
                            ),
                            4
                        ),

                    "F1":
                        round(
                            f1_score(
                                y_test,
                                predictions,
                                average="macro"
                            ),
                            4
                        )
                }

        return results