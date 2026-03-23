ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Install uv (via pip if not already available in base image)
RUN python -m pip install --no-cache-dir uv || true

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy bot package
COPY bot ./bot

# Sync dependencies into .venv
RUN uv sync --frozen --no-dev

# Use .venv
ENV PATH="/app/.venv/bin:$PATH"

# Run bot in polling mode
CMD ["python", "-m", "bot.bot"]
