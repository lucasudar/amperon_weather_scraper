FROM python:3.11.7-slim

# Set working directory
WORKDIR /app

# Environment variables to avoid Python and pip warnings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install Python dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc && \
python -m pip install --upgrade pip && \
python -m pip install -r requirements.txt

# Copy the application code
COPY tomorrow /app/tomorrow

# Set the default command
CMD ["python", "-m", "tomorrow"]