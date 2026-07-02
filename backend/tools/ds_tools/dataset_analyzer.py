import pandas as pd


class DatasetAnalyzer:

    def analyze(
        self,
        file_path: str
    ):

        df = pd.read_csv(file_path)

        numeric_df = df.select_dtypes(
            include="number"
        )


        report = {

            # =====================
            # BASIC INFO
            # =====================

            "shape": {
                "rows": len(df),
                "columns": len(df.columns)
            },

            "rows":
                len(df),

            "columns":
                len(df.columns),

            "column_names":
                list(df.columns),

            "data_types":
                df.dtypes.astype(str).to_dict(),

            "memory_usage":
                df.memory_usage(
                    deep=True
                ).to_dict(),

            # =====================
            # PREVIEW
            # =====================

            "head":
                df.head().to_dict(),

            "tail":
                df.tail().to_dict(),

            "sample":
                df.sample(
                    min(5, len(df))
                ).to_dict(),

            # =====================
            # DATA QUALITY
            # =====================

            "missing_values":
                df.isnull().sum().to_dict(),

            "missing_percentage":
                (
                    df.isnull().sum()
                    /
                    len(df)
                    *
                    100
                ).round(2).to_dict(),

            "duplicate_rows":
                int(
                    df.duplicated().sum()
                ),

            # =====================
            # STATISTICS
            # =====================

            "describe":
                df.describe(
                    include="all"
                ).fillna(
                    ""
                ).to_dict(),

            "mean":
                numeric_df.mean().to_dict(),

            "median":
                numeric_df.median().to_dict(),

            "mode":
                df.mode()
                .head(1)
                .fillna("")
                .to_dict(),

            "std":
                numeric_df.std().to_dict(),

            "variance":
                numeric_df.var().to_dict(),

            "min":
                numeric_df.min().to_dict(),

            "max":
                numeric_df.max().to_dict(),

            "range":
                (
                    numeric_df.max()
                    -
                    numeric_df.min()
                ).to_dict(),

            # =====================
            # DISTRIBUTION
            # =====================

            "skewness":
                numeric_df.skew().to_dict(),

            "kurtosis":
                numeric_df.kurt().to_dict(),

            "quantiles":
                numeric_df.quantile(
                    [0.25, 0.5, 0.75]
                ).to_dict(),

            # =====================
            # CORRELATION
            # =====================

            "correlation":
                numeric_df.corr().to_dict(),

            # =====================
            # CATEGORICAL ANALYSIS
            # =====================

            "unique_values":
                {
                    col:
                    int(
                        df[col].nunique()
                    )
                    for col in df.columns
                },

            "value_counts":
                {
                    col:
                    df[col]
                    .value_counts()
                    .head(10)
                    .to_dict()

                    for col in
                    df.select_dtypes(
                        include=[
                            "object",
                            "category"
                        ]
                    ).columns
                },

            # =====================
            # DATA QUALITY
            # =====================

            "constant_columns":
                [

                    col

                    for col in df.columns

                    if df[col].nunique()
                    == 1

                ],

            "high_cardinality_columns":
                [

                    col

                    for col in df.columns

                    if df[col].nunique()
                    > 100

                ],

            # =====================
            # COLUMN REPORT
            # =====================

            "column_report":

                {

                    col: {

                        "dtype":
                            str(
                                df[col].dtype
                            ),

                        "missing":
                            int(
                                df[col]
                                .isnull()
                                .sum()
                            ),

                        "unique":
                            int(
                                df[col]
                                .nunique()
                            )
                    }

                    for col in df.columns

                }
        }

        return report