# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Docker CLI and other dependencies
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY src/ ./src/

# Expose port 5000
EXPOSE 5000

# Command to run the application with Uvicorn
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "5000"]