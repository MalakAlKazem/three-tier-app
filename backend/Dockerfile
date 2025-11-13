# Use official Python runtime as the base image
FROM python:3.12-slim

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose the Flask port
EXPOSE 5000

# Run the Flask application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--log-level", "info", "app:app"]