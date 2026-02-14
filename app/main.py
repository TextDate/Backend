import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

# Debug: Print working directory and check model files at startup
print(f"=== STARTUP DEBUG ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"DECADE setting: {settings.decade}")
print(f"CENTURY setting: {settings.century}")
print(f"Decade model exists: {os.path.isfile(settings.decade)}")
print(f"Century model exists: {os.path.isfile(settings.century)}")
if os.path.exists('saved_models'):
    print(f"saved_models contents: {os.listdir('saved_models')}")
    if os.path.exists('saved_models/decades'):
        print(f"saved_models/decades contents: {os.listdir('saved_models/decades')}")
print(f"=== END DEBUG ===")

app = FastAPI(
    title="TextDate Predictor API",
    description="Predicts the age of a given text using pre-trained tree models.",
    version="1.0.0"
)

app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Health check endpoint for Railway/container orchestration."""
    return {"status": "healthy"}