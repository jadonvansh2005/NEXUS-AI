from sklearn.naive_bayes import (
    MultinomialNB
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.svm import (
    LinearSVC
)


class NLPModelTrainer:

    def train_models(
        self,
        X_train,
        y_train
    ):

        models = {

            "NaiveBayes":
                MultinomialNB(),

            "LogisticRegression":
                LogisticRegression(
                    max_iter=1000
                ),

            "LinearSVC":
                LinearSVC()

        }

        trained = {}

        for name, model in models.items():

            model.fit(
                X_train,
                y_train
            )

            trained[name] = model

        return trained