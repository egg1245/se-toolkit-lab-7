ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Install uv - try different methods for offline/online compatibility
# Method 1: Try apt package first (if system has it cached)
# Method 2: Fall back to pip if available
RUN apt-get update && apt-get install -y --no-install-recommends uv 2>/dev/null || \
    python -m pip install --no-cache-dir uv || \
    echo "Warning: uv installation may have failed, proceeding anyway"

# Copy project files
COPY pyproject.toml uv.lock ./
COPY bot ./bot

# Sync dependencies - use existing lockfile for reproducibility
RUN uv sync --frozen --no-dev

# Run bot in polling mode
CMD ["uv", "run", "python", "-m", "bot.bot"]
