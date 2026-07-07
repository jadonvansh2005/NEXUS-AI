import pandas as pd

from tools.ml_tools.text_cleaner import (
    TextCleaner
)


class DataCleaner:

    # =====================================================
    # Remove Constant Columns
    # =====================================================

    def _remove_constant_columns(
        self,
        df: pd.DataFrame
    ):

        constant_cols = [

            col

            for col in df.columns

            if df[col].nunique(
                dropna=False
            ) <= 1

        ]

        if constant_cols:

            print(
                "Removing Constant Columns:",
                constant_cols
            )

            df = df.drop(
                columns=constant_cols
            )

        return df

    # =====================================================
    # Remove High Missing Columns
    # =====================================================

    def _remove_high_missing_columns(

        self,

        df: pd.DataFrame,

        threshold: float = 0.70

    ):

        drop_cols = []

        for col in df.columns:

            missing_ratio = (

                df[col]
                .isna()
                .mean()

            )

            if missing_ratio >= threshold:

                drop_cols.append(col)

        if drop_cols:

            print(
                "Removing High Missing Columns:",
                drop_cols
            )

            df = df.drop(
                columns=drop_cols
            )

        return df

    # =====================================================
    # Main Cleaning Pipeline
    # =====================================================

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
        # Remove Constant Columns
        # ==================

        df = self._remove_constant_columns(
            df
        )

        # ==================
        # Remove High Missing Columns
        # ==================

        df = self._remove_high_missing_columns(
            df
        )

        # ==================
        # Datetime Conversion
        # ==================

        for col in df.columns:

            if pd.api.types.is_object_dtype(
                df[col]
            ):

                try:

                    converted = pd.to_datetime(

                        df[col],

                        errors="raise"

                    )

                    df[col] = (

                        converted.astype(
                            "int64"
                        ) // 10**9

                    )

                    print(
                        f"Datetime Converted: {col}"
                    )

                except Exception:

                    pass

        # ==================
        # Fill Missing Values
        # ==================

        for col in df.columns:

            if pd.api.types.is_numeric_dtype(
                df[col]
            ):

                median = (
                    df[col]
                    .median()
                )

                df[col] = (

                    df[col]
                    .fillna(
                        median
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

            print(
                "Removing ID Columns:",
                drop_cols
            )

            df = df.drop(

                columns=drop_cols

            )

        # ==================
        # Outlier Clipping
        # ==================

        for col in df.select_dtypes(
            include="number"
        ).columns:

            q1 = df[col].quantile(
                0.25
            )

            q3 = df[col].quantile(
                0.75
            )

            iqr = q3 - q1

            if iqr == 0:

                continue

            lower = (
                q1
                - 1.5 * iqr
            )

            upper = (
                q3
                + 1.5 * iqr
            )

            df[col] = df[col].clip(

                lower,

                upper

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

                    print(
                        f"Cleaning Text Column: {col}"
                    )

                    df[col] = (

                        df[col]

                        .astype(str)

                        .apply(

                            cleaner.clean_text

                        )

                    )

        print(
            "\nData Cleaning Completed."
        )

        return df