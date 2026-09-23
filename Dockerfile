FROM python:3.10-slim

# Install system dependencies for OpenCV and curl
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements file
COPY requirment.txt .
RUN pip install --no-cache-dir -r requirment.txt fastapi uvicorn python-multipart

# Download model.h5 directly from your GitHub Release
RUN curl -L -o model.h5 "https://github.com/rafayuchiha/cg-api/releases/download/v1.0/model.h5"

# Copy application code
COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]