from pydantic import BaseModel
from fastapi import UploadFile, File, Form
from typing import List

class Prediction(BaseModel):
    label: str
    probability: float


class FileUploadInput:
    def __init__(self, file: UploadFile = File(...), model_key: str = Form(...)):
        self.file = file
        self.model_key = model_key

class PredictionResponse(BaseModel):
    model_type: str
    top_k_predictions: List[Prediction]