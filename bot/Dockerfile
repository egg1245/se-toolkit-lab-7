ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Install uv once
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY bot ./bot

# Sync dependencies - use existing lockfile for reproducibility
RUN uv sync --frozen --no-dev

# Run bot in polling mode
CMD ["uv", "run", "python", "-m", "bot.bot"]
