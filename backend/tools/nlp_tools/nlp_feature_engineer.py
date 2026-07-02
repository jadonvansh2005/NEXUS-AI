from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


class NLPFeatureEngineer:

    def process(
        self,
        df,
        text_column,
        target
    ):

        vectorizer = (
            TfidfVectorizer(
                max_features=5000
            )
        )

        X = vectorizer.fit_transform(
            df[text_column]
            .astype(str)
        )

        y = df[target]

        return {

            "X":
                X,

            "y":
                y,

            "vectorizer":
                vectorizer

        }