import os
import joblib
import numpy as np
from app.core.config import settings
from fastapi import HTTPException
from app.utils.feature_extractor import extract_features_from_text
from app.utils.prediction_info import get_top_k_predictions

loaded_models = {}

def prepare_model_and_features(text: str, model_type: str):
    try:
        # Load model and metadata
        model, label_encoder, feature_names = load_model(model_type)

        # Extract features
        feature_values_raw = extract_features_from_text(text)
        if not feature_values_raw:
            raise ValueError("No features were extracted from the text.")

        # Align feature order
        feature_values = np.array([[feature_values_raw.get(feat, 0.0) for feat in feature_names]])

        # Predict top labels and probabilities
        top_predictions = get_top_k_predictions(model, label_encoder, feature_values, model_type)

        return model, label_encoder, top_predictions, feature_values

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model preparation or prediction failed: {str(e)}")

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