import pandas as pd


class PredictionPreprocessor:

    def prepare(
        self,
        df,
        metadata
    ):

        expected_columns = (
            metadata[
                "feature_names"
            ]
        )

        # --------------------
        # One Hot Encoding
        # --------------------

        df = pd.get_dummies(
            df
        )

        # --------------------
        # Add Missing Columns
        # --------------------

        for col in expected_columns:

            if col not in df.columns:

                df[col] = 0

        # --------------------
        # Remove Extra Columns
        # --------------------

        df = df[
            expected_columns
        ]

        return df