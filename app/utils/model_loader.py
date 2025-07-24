import os
import joblib
from app.core.config import settings
from fastapi import HTTPException

loaded_models = {}

def load_model(model_key: str):
    try:
        if model_key not in loaded_models:
            model_path = getattr(settings, model_key, None)
            if not model_path:
                raise ValueError(f"Missing model path for key: '{model_key}' in settings.")

            if not os.path.isfile(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")

            model_data = joblib.load(model_path)

            if not isinstance(model_data, tuple) or len(model_data) != 3:
                raise ValueError(f"Corrupt model file: expected a 3-element tuple, got {type(model_data)}")

            model, label_encoder, feature_names = model_data
            loaded_models[model_key] = (model, label_encoder, feature_names)

        return loaded_models[model_key]

    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Model loading error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error loading model '{model_key}': {str(e)}")