from fastapi import HTTPException
from app.utils.model_loader import prepare_model_and_features

def predict_binary_label(text: str, model_type: str = "decade", threshold: int = 1810) -> dict:
    try:
        model, label_encoder, top_predictions, feature_values = prepare_model_and_features(text, model_type)

        top_label = str(top_predictions[0][0])
        top_prob = float(top_predictions[0][1])

        try:
            top_decade = int(top_label)
        except ValueError:
            raise ValueError(f"Top label '{top_label}' could not be converted to an integer.")

        prediction = "older" if top_decade < threshold else "equal or younger"

        return {
            "prediction": prediction,
            "top_decade": top_decade,
            "top_probability": top_prob,
            "threshold": threshold
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")