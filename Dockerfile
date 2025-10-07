# Multi-stage Dockerfile for Magentic-Groq-UI
FROM node:18-alpine AS frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile

COPY frontend/ ./
RUN yarn build

# Python backend stage
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy application source
COPY src/ ./src/
COPY --from=frontend-builder /app/frontend/public ./src/magentic_groq_ui/backend/web/ui/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8081/api/health || exit 1

# Start application
CMD ["magentic-groq-ui", "--port", "8081", "--host", "0.0.0.0"]
