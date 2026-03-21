FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy pyproject.toml and uv.lock from repo root
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies with uv (caches dependencies layer)
RUN uv sync --frozen

# Copy bot source code
COPY bot bot

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Run bot using uv
CMD ["uv", "run", "python", "-m", "bot.bot"]
