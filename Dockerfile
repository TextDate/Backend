# Backend/Dockerfile

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install git and pip dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords

# Copy app code
COPY . .

# Debug: List model files to verify they were copied
RUN echo "=== Checking saved_models directory ===" && \
    ls -la saved_models/ && \
    ls -la saved_models/decades/ && \
    ls -la saved_models/centuries/

# Use uvicorn to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050", "--reload"]