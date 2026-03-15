FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (gcc may be needed for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories for any static files (optional, for local testing)
RUN mkdir -p static/comics static/uploads

# Corrected CMD – point to main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
