FROM python:3.10-slim

# Set environment variables to reduce Python buffering and enable Docker build output to be seen in real time
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for compiling Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    # If you have other dependencies that require system libraries, install them here
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry for dependency management
RUN pip install poetry

# Disable virtual env creation by poetry, we want the packages to be installed globally in the docker image
RUN poetry config virtualenvs.create false

# Install the dependencies
RUN poetry install

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
