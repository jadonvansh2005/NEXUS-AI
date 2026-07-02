import pandas as pd


class NLPDetector:

    def detect(
        self,
        df: pd.DataFrame
    ):

        text_columns = []

        print(
            "\n========== NLP DETECTOR DEBUG =========="
        )

        for col in df.columns:

            # Only check string/object columns
            if not (

                pd.api.types.is_object_dtype(
                    df[col]
                )

                or

                pd.api.types.is_string_dtype(
                    df[col]
                )

            ):
                continue

            sample = (

                df[col]
                .dropna()
                .astype(str)

            )

            if len(sample) == 0:
                continue

            avg_len = (
                sample
                .str.len()
                .mean()
            )

            unique_ratio = (

                sample.nunique()
                / len(sample)

            )

            space_ratio = (

                sample
                .str.contains(
                    " ",
                    regex=False
                )
                .mean()

            )

            print(
                f"\nCOLUMN: {col}"
            )

            print(
                "AVG_LEN:",
                round(
                    avg_len,
                    2
                )
            )

            print(
                "UNIQUE_RATIO:",
                round(
                    unique_ratio,
                    4
                )
            )

            print(
                "SPACE_RATIO:",
                round(
                    space_ratio,
                    4
                )
            )

            # NLP Detection Rules
            if (

                avg_len > 15

                or

                unique_ratio > 0.50

                or

                space_ratio > 0.50

            ):

                text_columns.append(
                    col
                )

            print(
                "DETECTED AS NLP:",
                col in text_columns
            )

        print(
            "\nTEXT COLUMNS DETECTED:"
        )

        print(
            text_columns
        )

        print(
            "========================================\n"
        )

        return {

            "is_nlp":
                len(
                    text_columns
                ) > 0,

            "text_columns":
                text_columns

        }