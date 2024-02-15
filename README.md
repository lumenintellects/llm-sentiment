# llm-sentiment
This project is a FastAPI-based sentiment analysis service using a Hugging Face transformers model, containerized with Docker and deployable on Kubernetes, featuring automated testing and MLflow integration for performance tracking.

## Features

- **FastAPI for REST API**: High performance, easy to use framework for building APIs.
- **Hugging Face Transformers**: Utilize powerful pre-trained models for sentiment analysis.
- **Docker and Kubernetes**: Containerization and orchestration support for easy deployment and scalability.
- **Poetry for Dependency Management**: Reproducible builds and straightforward dependency management.
- **Automated Testing**: Includes tests for API functionality and model performance evaluation.
- **MLflow Integration**: Track model performance metrics for continuous improvement.

## Setup and Installation

1. **Clone the Repository**


    git clone <repository-url>

## Install Dependencies

Ensure that Poetry is installed on your system. Then, in the project directory, run:

    poetry install

## Environment Variables

Create a `.env` file in the root directory and specify the following variables:

- `MODEL_NAME`: The name of the pre-trained model from Hugging Face.
- `MLFLOW_URL`: The URL for MLflow tracking server.
- `PREDICT_URL`: The URL for the FastAPI prediction endpoint.

## Run the Application

Use the following command to run the FastAPI application:
    
    poetry run uvicorn main:app --reload

## Deployment

Refer to the Kubernetes manifests (fastapi_deployment.yaml, fastapi_hpa.yaml, fastapi_service.yaml) for deploying the application to a Kubernetes cluster. Ensure Docker is installed and configured for building and pushing the container image.

## Testing

To run the tests, execute the following command:

    poetry run pytest
