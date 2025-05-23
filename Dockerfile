# Use Python 3.8 slim image with security updates
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies with security updates
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Install Python dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose port (will be overridden by docker-compose)
EXPOSE ${PORT:-8000}

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"] 