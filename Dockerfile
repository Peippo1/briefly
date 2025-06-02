# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variables (note: .env is passed at runtime)
ENV PYTHONUNBUFFERED=1

# Run Streamlit app
CMD ["streamlit", "run", "webapp/app.py", "--server.port=8501", "--server.enableCORS=false"]