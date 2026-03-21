FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy pyproject.toml and uv.lock for dependency caching
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies with uv
RUN uv sync --frozen

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Run bot - use full module path
CMD ["uv", "run", "python", "-m", "bot.bot"]
