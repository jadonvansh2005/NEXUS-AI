class ModelSelector:

    def select_best(
        self,
        results,
        problem_type
    ):

        if problem_type == "regression":

            metric = "R2"

        else:

            metric = "Accuracy"

        best_model = max(
            results,
            key=lambda x:
            results[x][metric]
        )

        return best_model