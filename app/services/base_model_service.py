from fastapi import HTTPException
from app.utils.model_loader import prepare_model_and_features

def predict_base_label(text: str, model_type: str = "decade") -> dict:
    try:
        model, label_encoder, top_predictions, feature_values = prepare_model_and_features(text, model_type)
        return {
            "top_k_predictions": [
                {"label": str(label), "probability": float(prob)}
                for label, prob in top_predictions
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")