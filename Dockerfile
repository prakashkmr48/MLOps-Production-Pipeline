# Multi-stage Docker build for ML model serving
# Stage 1: Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \n    gcc \n    g++ \n    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.9-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 mlops && \n    chown -R mlops:mlops /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/mlops/.local

# Copy application code
COPY --chown=mlops:mlops . .

# Set environment variables
ENV PATH=/home/mlops/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models

# Switch to non-root user
USER mlops

# Expose port for FastAPI
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
