# Use the official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and upgrade pip
RUN apt-get update && \
    apt-get install -y gcc python3-dev libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip

# Copy the application code into the container
COPY . /app

# Create a virtual environment in .venv
RUN python -m venv .venv

# Install Python dependencies from requirements.txt
RUN /bin/bash -c "source .venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Expose FastAPI's default port
EXPOSE 8000

# Command to run the FastAPI application
# CMD ["venv/bin/uvicorn", "unface:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["/bin/bash", "-c", "source .venv/bin/activate && uvicorn unface:app --host 0.0.0.0 --port 8000"]