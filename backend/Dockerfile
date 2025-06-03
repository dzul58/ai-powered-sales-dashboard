# Gunakan Python 3.11 sebagai base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first untuk memanfaatkan Docker cache
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY backend/ .

# Expose port yang digunakan
EXPOSE 8000

# Command untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 