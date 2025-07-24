import numpy as np
from fastapi import HTTPException
from app.utils.feature_extractor import extract_features_from_text
from app.utils.model_loader import load_model
from app.utils.prediction_info import get_top_k_predictions

def predict_label(text: str, model_type: str = "decade") -> dict:
    try:
        model, label_encoder, feature_names = load_model(model_type)

        feature_values_raw = extract_features_from_text(text)
        if not feature_values_raw:
            raise ValueError("No features were extracted from the text.")

        feature_values = np.array([[feature_values_raw.get(feat, 0.0) for feat in feature_names]])

        top_predictions = get_top_k_predictions(model, label_encoder, feature_values, model_type)

        return {
            "top_k_predictions": [
                {"label": str(label), "probability": float(prob)}
                for label, prob in top_predictions
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")