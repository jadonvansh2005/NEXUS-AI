import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

from sklearn.feature_selection import (
    mutual_info_regression,
    mutual_info_classif
)


class FeatureEngineer:

    def process(
        self,
        df,
        target,
        problem_type
    ):

        df = df.copy()

        # =====================
        # Missing Value Handling
        # =====================

        for col in df.columns:

            if pd.api.types.is_numeric_dtype(
                df[col]
            ):

                df[col] = (
                    df[col]
                    .fillna(
                        df[col].median()
                    )
                )

            else:

                df[col] = (
                    df[col]
                    .fillna(
                        "Unknown"
                    )
                )

        # =====================
        # Separate Target
        # =====================

        y = df[target]

        X = df.drop(
            columns=[target]
        )

        # =====================
        # Detect NLP Dataset
        # =====================

#         text_cols = []

#         for col in X.columns:

#             if not pd.api.types.is_numeric_dtype(
#                 X[col]
#             ):

#                 avg_len = (

#                     X[col]
#                     .astype(str)
#                     .str.len()
#                     .mean()

#                 )

#                 unique_ratio = (

#                     X[col]
#                     .nunique()

#                     / max(
#                         len(X),
#                         1
#                     )

#                 )

#                 if (

#                     avg_len > 20

#                     or

#                     unique_ratio > 0.5

#                 ):

#                     text_cols.append(
#                         col
#                     )

#         if len(text_cols) > 0:

#             raise ValueError(

#                 f"""
# NLP Dataset Detected.

# Text Columns:
# {text_cols}

# Current AutoML supports only structured/tabular datasets.

# Route this dataset to NLP Pipeline.
# """

#             )

        # =====================
        # Categorical Columns
        # =====================

        categorical_cols = [

            col

            for col in X.columns

            if not pd.api.types.is_numeric_dtype(
                X[col]
            )

        ]

        # =====================
        # Binary Encoding
        # =====================

        binary_cols = [

            col

            for col in categorical_cols

            if X[col].nunique() == 2

        ]

        for col in binary_cols:

            encoder = LabelEncoder()

            X[col] = encoder.fit_transform(
                X[col]
                .astype(str)
            )

        # =====================
        # One Hot Encoding
        # =====================

        multi_class_cols = [

            col

            for col in categorical_cols

            if X[col].nunique() > 2

        ]

        if len(
            multi_class_cols
        ) > 0:

            X = pd.get_dummies(

                X,

                columns=multi_class_cols,

                drop_first=True,

                dtype=int

            )

        # =====================
        # Final Safety Check
        # =====================

        object_cols = (

            X.select_dtypes(

                include=[
                    "object",
                    "string"
                ]

            )
            .columns
            .tolist()

        )

        if len(
            object_cols
        ) > 0:

            raise ValueError(

                f"""
Unsupported Columns Found After Encoding:

{object_cols}

All features must be numeric before scaling.
"""

            )

        # =====================
        # Scaling
        # =====================

        scaler = (
            StandardScaler()
        )

        X_scaled = pd.DataFrame(

            scaler.fit_transform(
                X
            ),

            columns=X.columns

        )

        # =====================
        # Target Encoding
        # =====================

        if problem_type == "classification":

            if not pd.api.types.is_numeric_dtype(
                y
            ):

                target_encoder = (
                    LabelEncoder()
                )

                y = (

                    target_encoder
                    .fit_transform(
                        y.astype(str)
                    )

                )

        # =====================
        # Feature Importance
        # =====================

        try:

            if problem_type == "regression":

                scores = (

                    mutual_info_regression(

                        X_scaled,

                        y,

                        random_state=42

                    )

                )

            else:

                scores = (

                    mutual_info_classif(

                        X_scaled,

                        y,

                        random_state=42

                    )

                )

        except Exception:

            scores = [

                0.0

                for _ in range(
                    len(
                        X_scaled.columns
                    )
                )

            ]

        feature_scores = {

            col: float(
                round(
                    score,
                    4
                )
            )

            for col, score in zip(

                X_scaled.columns,

                scores

            )

        }

        feature_scores = dict(

            sorted(

                feature_scores.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )

        return {

            "X":
                X_scaled,

            "y":
                y,

            "scaler":
                scaler,

            "feature_scores":
                feature_scores,

            "feature_count":
                len(
                    X_scaled.columns
                ),

            "selected_columns":
                list(
                    X_scaled.columns
                )

        }