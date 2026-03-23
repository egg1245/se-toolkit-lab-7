ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/

# Build stage: prepare dependencies with uv
FROM ${REGISTRY_PREFIX}python:3.11-slim AS builder

WORKDIR /app

# Install uv via pip (only in builder, not in runtime)
RUN python -m pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy bot package
COPY bot ./bot

# Sync dependencies into .venv
RUN uv sync --frozen --no-dev

# Runtime stage: minimal image with .venv
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Copy .venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy bot package
COPY bot ./bot

# Use .venv from builder
ENV PATH="/app/.venv/bin:$PATH"

# Run bot in polling mode
CMD ["python", "-m", "bot.bot"]
