FROM ubuntu:20.04
COPY --from=docker/buildx-bin /buildx /usr/libexec/docker/cli-plugins/docker-buildx
RUN docker buildx version

# Use a Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies and set up venv
# RUN python -m venv .venv
RUN apt-get install gcc python3-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI's default port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["venv/bin/uvicorn", "unface:app", "--host", "0.0.0.0", "--port", "8000"]