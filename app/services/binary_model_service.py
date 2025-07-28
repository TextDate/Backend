from fastapi import HTTPException
from app.utils.model_loader import prepare_model_and_features
import logging

logger = logging.getLogger(__name__)

def predict_binary_label(text: str, threshold: int, model_type: str = "decade",) -> dict:
    try:
        model, label_encoder, top_predictions, feature_values = prepare_model_and_features(text, model_type)

        if not top_predictions:
            raise ValueError("No predictions were returned.")

        older = []
        younger_or_equal = []

        for label, probability in top_predictions:
            try:
                label_int = int(label)
                entry = {"label": str(label), "probability": float(probability)}
                if label_int < threshold:
                    older.append(entry)
                else:
                    younger_or_equal.append(entry)
            except ValueError:
                logger.warning(f"Skipping invalid label: {label}")
                continue

        older_total = sum(item["probability"] for item in older)
        younger_total = sum(item["probability"] for item in younger_or_equal)

        prediction = "older" if older_total > younger_total else "equal or younger"

        return {
            "prediction": prediction,
            "top_k": {
                "older": {
                    "total_probability": older_total,
                    "items": older
                },
                "equal_or_younger": {
                    "total_probability": younger_total,
                    "items": younger_or_equal
                }
            }
        }

    except Exception as e:
        logger.exception("Binary prediction failed.")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")