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

# Use uvicorn to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]