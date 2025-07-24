from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="TextDate Predictor API",
    description="Predicts the age of a given text using pre-trained tree models.",
    version="1.0.0"
)

app.include_router(api_router)