import numpy as np
from fastapi import HTTPException

def get_top_k_predictions(model, label_encoder, features, model_type: str):
    """
    Given a model and input features, returns the top-K (label, probability) predictions.
    Top-K is 10 for 'decade' models, 2 otherwise.
    """
    try:
        if features is None:
            raise ValueError("Input features are None.")

        if not hasattr(model, "predict_proba"):
            raise ValueError("Model does not support probability predictions.")

        probabilities = model.predict_proba(features)[0]

        top_k = 10 if "decade" in model_type.lower() else 2

        top_indices = np.argsort(probabilities)[::-1][:top_k]

        top_labels = label_encoder.inverse_transform(top_indices)
        top_probs = probabilities[top_indices]

        return list(zip(top_labels, top_probs))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")