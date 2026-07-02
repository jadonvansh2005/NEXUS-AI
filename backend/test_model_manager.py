from sklearn.ensemble import (
    RandomForestClassifier
)

from tools.ml_tools.model_manager import (
    ModelManager
)

manager = ModelManager()

model = RandomForestClassifier()

path = manager.save_model(
    model,
    "test_model"
)

print(path)

print(
    manager.list_models()
)