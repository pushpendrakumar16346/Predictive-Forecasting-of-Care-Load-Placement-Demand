
from pathlib import Path
import os
import pickle
import joblib
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

SUPPORTED_EXTENSIONS = {".joblib", ".pkl", ".pickle"}

def discover_models(model_directory=None):
    directory = Path(model_directory or MODEL_DIR)

    if not directory.exists():
        return []

    return sorted(
        path for path in directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
        and "registry" not in path.parts
    )

def load_model(model_path=None, model_name=None):
    selected_path = model_path or os.getenv("FORECAST_MODEL_PATH")

    if selected_path:
        path = Path(selected_path)

        if not path.is_absolute():
            path = PROJECT_ROOT / path
    else:
        available = discover_models()

        if model_name:
            available = [
                item for item in available
                if item.name == model_name or item.stem == model_name
            ]

        if len(available) == 0:
            raise FileNotFoundError(
                "No supported trained model was found."
            )

        if len(available) > 1:
            raise RuntimeError(
                "Multiple model artifacts found. Specify the exact path."
            )

        path = available[0]

    if not path.exists():
        raise FileNotFoundError(f"Model does not exist: {path}")

    if path.suffix.lower() == ".joblib":
        model = joblib.load(path)
    elif path.suffix.lower() in {".pkl", ".pickle"}:
        with open(path, "rb") as file:
            model = pickle.load(file)
    else:
        raise ValueError("Unsupported model format.")

    return model

def predict_with_model(model, features):
    if not hasattr(model, "predict"):
        raise TypeError("Model does not expose predict().")

    return model.predict(features)

def load_project_config(environment=None):
    environment = (
        environment or os.getenv("APP_ENV", "development")
    ).lower()

    if environment not in {"development", "production"}:
        raise ValueError("Invalid APP_ENV.")

    config_path = PROJECT_ROOT / "config" / f"{environment}.json"

    with open(config_path, encoding="utf-8") as file:
        return json.load(file)
