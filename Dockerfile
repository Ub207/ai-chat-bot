FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements_hf.txt .
RUN pip install --no-cache-dir -r requirements_hf.txt

# Copy the rest of the application
COPY . .

# Ensure /tmp is available for database
RUN mkdir -p /tmp

# Expose the port Hugging Face Spaces uses
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Command to run the application
CMD ["python", "app_hf.py"]