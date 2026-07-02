import pandas as pd

from tools.ml_tools.text_cleaner import (
    TextCleaner
)


class DataCleaner:

    def clean(
        self,
        df: pd.DataFrame
    ):

        cleaner = (
            TextCleaner()
        )

        # ==================
        # Remove Duplicates
        # ==================

        df = df.drop_duplicates()

        # ==================
        # Fill Missing Values
        # ==================

        for col in df.columns:

            if pd.api.types.is_numeric_dtype(
                df[col]
            ):

                df[col] = (

                    df[col]
                    .fillna(

                        df[col]
                        .median()

                    )

                )

            else:

                df[col] = (

                    df[col]
                    .fillna(
                        "Unknown"
                    )

                )

        # ==================
        # Remove ID Columns
        # ==================

        drop_cols = []

        for col in df.columns:

            if (
                "id"
                in col.lower()
            ):

                drop_cols.append(
                    col
                )

        if drop_cols:

            df = df.drop(
                columns=drop_cols
            )

        # ==================
        # Clean Long Text
        # ==================

        for col in df.columns:

            if (
                pd.api.types.is_string_dtype(
                    df[col]
                )
            ):

                avg_len = (

                    df[col]
                    .astype(str)
                    .str.len()
                    .mean()

                )

                if avg_len > 20:

                    df[col] = (

                        df[col]
                        .astype(str)
                        .apply(
                            cleaner.clean_text
                        )

                    )
        return df