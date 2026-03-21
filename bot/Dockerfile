FROM python:3.11-slim

WORKDIR /app

# Install uv once
RUN pip install --no-cache-dir uv

# Copy entire project structure for uv sync
COPY pyproject.toml uv.lock ./
COPY bot ./bot

# Sync dependencies (both root and bot pyproject.toml)
# Use --frozen to use existing lockfile, --no-dev to skip dev dependencies
RUN uv sync --frozen --no-dev || true

# Run bot
CMD ["uv", "run", "python", "-m", "bot.bot"]
