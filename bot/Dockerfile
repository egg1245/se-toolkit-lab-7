ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/

# Stage 1: Get uv from official image (don't use registry prefix for ghcr.io)
FROM ghcr.io/astral-sh/uv:latest AS uv-builder

# Stage 2: Build app with python base image
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Copy uv binary from builder stage
COPY --from=uv-builder /usr/local/bin/uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY bot ./bot

# Sync dependencies - use existing lockfile for reproducibility
RUN uv sync --frozen --no-dev

# Run bot in polling mode
CMD ["uv", "run", "python", "-m", "bot.bot"]
