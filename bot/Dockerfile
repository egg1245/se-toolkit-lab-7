ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.11-slim

WORKDIR /app

# Copy bot package
COPY bot ./bot

# Install bot dependencies
RUN pip install --no-cache-dir \
    python-telegram-bot>=20.0 \
    httpx>=0.25.0 \
    pydantic-settings>=2.0.0 \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0

# Run bot in polling mode
CMD ["python", "-m", "bot.bot"]
