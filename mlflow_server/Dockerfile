FROM python:3.11-slim

WORKDIR /mlflow

# Install MLflow and dependencies
RUN pip install --no-cache-dir \
    mlflow==2.11.3 \
    psycopg2-binary==2.9.9 \
    boto3==1.34.0

# Create directories for MLflow data
RUN mkdir -p /mlflow/data /mlflow/artifacts

# Expose MLflow port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run MLflow server
# Using file-based backend store and artifact root
# Can be configured via environment variables
CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri ${MLFLOW_BACKEND_STORE_URI:-file:///mlflow/data} \
    --default-artifact-root ${MLFLOW_ARTIFACT_ROOT:-file:///mlflow/artifacts}

