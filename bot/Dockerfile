ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency lock file and project definition
COPY pyproject.toml uv.lock ./

# Copy bot package
COPY bot ./bot

# Sync dependencies - uses lock file for reproducibility
RUN uv sync --frozen --no-dev

# Run bot in polling mode
CMD ["uv", "run", "python", "-m", "bot.bot"]
