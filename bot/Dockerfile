ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Copy bot package
COPY bot ./bot

# Install bot dependencies
RUN python -m pip install --no-cache-dir -e ./bot

# Run bot in polling mode
CMD ["python", "-m", "bot.bot"]
