import numpy as np
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
)

from sklearn.feature_selection import (
    mutual_info_regression,
    mutual_info_classif,
    VarianceThreshold,
)


class FeatureEngineer:

    # =====================================================
    # Replace Rare Categories
    # =====================================================

    def _replace_rare_categories(

        self,

        df: pd.DataFrame,

        threshold: float = 0.01,

    ):

        df = df.copy()

        categorical = df.select_dtypes(

            include=[
                "object",
                "string"
            ]

        ).columns

        for col in categorical:

            freq = (

                df[col]

                .value_counts(

                    normalize=True

                )

            )

            rare = freq[

                freq < threshold

            ].index

            if len(rare):

                df[col] = (

                    df[col]

                    .replace(

                        rare,

                        "Other"

                    )

                )

        return df

    # =====================================================
    # Remove Near Zero Variance
    # =====================================================

    def _remove_low_variance(

        self,

        X,

    ):

        selector = (

            VarianceThreshold(

                threshold=0.0001

            )

        )

        selector.fit(X)

        selected = (

            X.columns[

                selector.get_support()

            ]

        )

        return X[selected]

    # =====================================================
    # Main Pipeline
    # =====================================================

    def process(

        self,

        df,

        target,

        problem_type,

    ):

        df = df.copy()

        # ==========================================
        # Boolean → Integer
        # ==========================================

        bool_cols = (

            df.select_dtypes(

                include="bool"

            ).columns

        )

        for col in bool_cols:

            df[col] = (

                df[col]

                .astype(int)

            )

        # ==========================================
        # Rare Category Handling
        # ==========================================

        df = self._replace_rare_categories(df)

        # ==========================================
        # Missing Values
        # ==========================================

        for col in df.columns:

            if (

                pd.api.types.is_numeric_dtype(

                    df[col]

                )

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

        # ==========================================
        # Separate Target
        # ==========================================

        y = df[target]

        X = df.drop(

            columns=[

                target

            ]

        )

        # ==========================================
        # Detect Categorical Columns
        # ==========================================

        categorical_cols = [

            col

            for col in X.columns

            if not pd.api.types.is_numeric_dtype(

                X[col]

            )

        ]

        # ==========================================
        # Binary Encoding
        # ==========================================

        binary_cols = [

            col

            for col in categorical_cols

            if X[col].nunique() == 2

        ]

        binary_encoders = {}

        for col in binary_cols:

            encoder = LabelEncoder()

            X[col] = (

                encoder.fit_transform(

                    X[col]

                    .astype(str)

                )

            )

            binary_encoders[col] = encoder

        # ==========================================
        # One Hot Encoding
        # ==========================================

        multi_class_cols = [

            col

            for col in categorical_cols

            if X[col].nunique() > 2

        ]

        if multi_class_cols:

            X = pd.get_dummies(

                X,

                columns=multi_class_cols,

                drop_first=True,

                dtype=int,

            )

        # ==========================================
        # Remove Near Zero Variance
        # ==========================================

        X = self._remove_low_variance(X)

        # ==========================================
        # Final Safety Check
        # ==========================================

        object_cols = (

            X.select_dtypes(

                include=[

                    "object",

                    "string",

                ]

            )

            .columns

            .tolist()

        )

        if object_cols:

            raise ValueError(

                f"""

Unsupported Columns Found

{object_cols}

"""

            )

        X = X.astype(float)



        # ==========================================
        # Scaling
        # ==========================================

        scaler = StandardScaler()

        X_scaled = pd.DataFrame(

            scaler.fit_transform(X),

            columns=X.columns,

        )

        # ==========================================
        # Target Encoding
        # ==========================================

        target_encoder = None

        if problem_type == "classification":

            if not pd.api.types.is_numeric_dtype(y):

                target_encoder = LabelEncoder()

                y = target_encoder.fit_transform(

                    y.astype(str)

                )

        # ==========================================
        # Feature Importance
        # ==========================================

        try:

            if problem_type == "regression":

                scores = mutual_info_regression(

                    X_scaled,

                    y,

                    random_state=42,

                )

            else:

                scores = mutual_info_classif(

                    X_scaled,

                    y,

                    random_state=42,

                )

        except Exception:

            scores = np.zeros(

                len(X_scaled.columns)

            )

        feature_scores = {

            feature: float(

                round(score, 5)

            )

            for feature, score

            in zip(

                X_scaled.columns,

                scores,

            )

        }

        feature_scores = dict(

            sorted(

                feature_scores.items(),

                key=lambda x: x[1],

                reverse=True,

            )

        )

        # ==========================================
        # Select Top Features
        # ==========================================

        top_features = list(

            feature_scores.keys()

        )[:25]

        # ==========================================
        # Metadata
        # ==========================================

        encoding_metadata = {

            "binary_encoded": binary_cols,

            "one_hot_encoded": multi_class_cols,

            "feature_columns": list(

                X_scaled.columns

            ),

        }

        # ==========================================
        # Return
        # ==========================================

        return {

            "X": X_scaled,

            "y": y,

            "scaler": scaler,

            "target_encoder": target_encoder,

            "binary_encoders": binary_encoders,

            "feature_scores": feature_scores,

            "top_features": top_features,

            "encoding_metadata": encoding_metadata,

            "feature_count": len(

                X_scaled.columns

            ),

            "selected_columns": list(

                X_scaled.columns

            ),

        }