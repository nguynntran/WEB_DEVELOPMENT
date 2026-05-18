FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create database directory
RUN mkdir -p /app/database

# Copy requirements file
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 5050

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the application using gunicorn for production. Use $PORT with a default of 8080.
CMD ["sh", "-c", "gunicorn 'run:app' --bind 0.0.0.0:${PORT:-8080} --workers 4"]
