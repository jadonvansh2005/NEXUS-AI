from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


class NLPEvaluator:

    def evaluate(
        self,
        models,
        X_test,
        y_test
    ):

        results = {}

        for name, model in models.items():

            pred = model.predict(
                X_test
            )

            results[name] = {

                "Accuracy":
                    round(
                        accuracy_score(
                            y_test,
                            pred
                        ),
                        4
                    ),

                "Precision":
                    round(
                        precision_score(
                            y_test,
                            pred,
                            average="weighted"
                        ),
                        4
                    ),

                "Recall":
                    round(
                        recall_score(
                            y_test,
                            pred,
                            average="weighted"
                        ),
                        4
                    ),

                "F1":
                    round(
                        f1_score(
                            y_test,
                            pred,
                            average="weighted"
                        ),
                        4
                    )
            }

        return results