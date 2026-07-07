from __future__ import annotations

import pandas as pd


class DatasetTypeDetector:
    """
    Detect whether an uploaded dataset belongs to:

    1. Structured ML Pipeline
    2. NLP Pipeline

    This detector avoids routing normal categorical datasets
    (Gender, City, Stream, etc.) into the NLP pipeline.
    """

    IGNORE_COLUMNS = {

        "id",
        "user_id",
        "userid",

        "name",
        "first_name",
        "last_name",

        "gender",
        "sex",

        "city",
        "state",
        "country",

        "college",
        "university",

        "department",
        "stream",
        "branch",
        "course",

        "category",

        "email",
        "phone",
        "mobile",

    }

    # ==========================================================
    # Ignore obvious categorical columns
    # ==========================================================

    def _is_ignored_column(
        self,
        column_name: str,
    ) -> bool:

        return column_name.lower().strip() in self.IGNORE_COLUMNS

    # ==========================================================
    # Detect Dataset Type
    # ==========================================================

    def detect(
        self,
        df: pd.DataFrame,
        target: str,
    ) -> dict:

        text_columns = []

        total_rows = max(len(df), 1)

        print("\n========== DATASET TYPE DETECTOR ==========")

        for col in df.columns:

            if col == target:
                continue

            if self._is_ignored_column(col):

                print(f"\nCOLUMN: {col}")
                print("Skipped (Known categorical column)")
                continue

            if not (

                pd.api.types.is_object_dtype(df[col])

                or

                pd.api.types.is_string_dtype(df[col])

            ):

                continue

            sample = (

                df[col]

                .dropna()

                .astype(str)

            )

            if sample.empty:
                continue

            avg_length = (

                sample
                .str.len()
                .mean()

            )

            median_length = (

                sample
                .str.len()
                .median()

            )

            max_length = (

                sample
                .str.len()
                .max()

            )

            unique_ratio = (

                sample.nunique()

                / total_rows

            )

            avg_words = (

                sample
                .str.split()
                .apply(len)
                .mean()

            )

            space_ratio = (

                sample
                .str.contains(
                    " ",
                    regex=False
                )
                .mean()

            )

            long_sentence_ratio = (

                sample
                .str.len()
                .gt(50)
                .mean()

            )

            unique_count = sample.nunique()

            # ==================================================
            # Production Scoring
            # ==================================================

            score = 0

            if avg_length > 30:
                score += 25

            if avg_words > 5:
                score += 20

            if unique_ratio > 0.10:
                score += 20

            if space_ratio > 0.50:
                score += 15

            if median_length > 25:
                score += 10

            if max_length > 100:
                score += 5

            if long_sentence_ratio > 0.30:
                score += 5

            # Penalize low-cardinality categorical columns
            if unique_count < 20:
                score -= 40

            # Penalize one-word categorical columns
            if avg_words <= 2:
                score -= 20

            print(f"\nCOLUMN: {col}")
            print("Average Length :", round(avg_length, 2))
            print("Median Length  :", round(median_length, 2))
            print("Max Length     :", max_length)
            print("Average Words  :", round(avg_words, 2))
            print("Unique Ratio   :", round(unique_ratio, 4))
            print("Unique Count   :", unique_count)
            print("Space Ratio    :", round(space_ratio, 4))
            print("Long Text %    :", round(long_sentence_ratio, 4))
            print("NLP Score      :", score)

            if score >= 60:

                print("Detected as NLP")

                text_columns.append(col)

            else:

                print("Detected as Structured")

        dataset_type = (

            "nlp"

            if text_columns

            else

            "structured"

        )

        confidence = (

            98

            if dataset_type == "nlp"

            else

            95

        )

        print("\n==========================================")
        print("DATASET TYPE :", dataset_type)
        print("CONFIDENCE   :", confidence)
        print("TEXT COLUMNS :", text_columns)
        print("==========================================\n")

        return {

            "dataset_type": dataset_type,

            "text_columns": text_columns,

            "is_nlp": dataset_type == "nlp",

            "confidence": confidence,

            "reason": (

                f"NLP columns detected: {text_columns}"

                if text_columns

                else

                "No long-form text columns detected."

            )

        }