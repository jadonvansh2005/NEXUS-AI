import pandas as pd


class TargetDetector:

    def detect(
        self,
        df: pd.DataFrame
    ):

        priority_targets = [

            "target",
            "label",
            "class",
            "output",
            "result",
            "response",
            "intent",
            "category",
            "spam",
            "sentiment"

        ]

        target_column = None

        for col in df.columns:

            if col.lower() in priority_targets:

                target_column = col
                break

        if target_column is None:

            target_column = (
                df.columns[-1]
            )

        unique_values = (
            df[target_column]
            .nunique()
        )

        if not pd.api.types.is_numeric_dtype(
            df[target_column]
        ):

            problem_type = (
                "classification"
            )

        elif unique_values <= 20:

            problem_type = (
                "classification"
            )

        else:

            problem_type = (
                "regression"
            )

        print(
            "\n========== TARGET DEBUG =========="
        )

        print(
            "TARGET COLUMN:",
            target_column
        )

        print(
            "PROBLEM TYPE:",
            problem_type
        )

        print(
            "UNIQUE VALUES:",
            unique_values
        )

        print(
            "TARGET DTYPE:",
            df[target_column].dtype
        )

        print(
            "==================================\n"
        )

        return {

            "target":
                target_column,

            "problem_type":
                problem_type,

            "unique_values":
                int(
                    unique_values
                )
        }