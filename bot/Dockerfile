FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy entire project for uv sync
COPY . .

# Sync dependencies using uv
RUN uv sync --frozen --no-dev

# Run bot
CMD ["uv", "run", "python", "-m", "bot.bot"]
