from tools.ml_tools.automl_engine import (
    AutoMLEngine
)

engine = (
    AutoMLEngine()
)

result = (
    engine.run(
        "uploads/datasets/fixed_spam_cleaned.csv"
    )
)

print(result)