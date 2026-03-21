# LMS Bot

Telegram bot for LMS (Learning Management System) integration with LLM-based intent routing.

## Quick Start

### Installation

```bash
cd bot
uv sync
```

### Test Mode (no Telegram required)

```bash
# Test individual commands
python bot.py --test "/start"
python bot.py --test "/help"
python bot.py --test "/health"
python bot.py --test "/labs"
python bot.py --test "/scores"
```

### Run Tests

```bash
cd ..  # Return to project root
uv run -p tests pytest tests/ -v
```

## Project Structure

```
bot/
├── bot.py                 # Entry point with --test mode
├── config.py              # Environment configuration (pydantic-settings)
├── handlers/              # Command handlers (pure functions)
│   ├── __init__.py
│   └── commands.py        # /start, /help, /health, /labs, /scores
├── services/              # External service clients
│   ├── __init__.py
│   ├── lms_client.py      # LMS API client (task-2)
│   └── llm_client.py      # LLM tool calling interface (task-3)
├── pyproject.toml         # Dependencies (uv-managed)
├── Dockerfile             # Docker image (task-4)
├── PLAN.md                # Architecture and design decisions
└── README.md              # This file
```

## Configuration

### Local Development

1. Create `.env.bot.secret` in project root (copy from `.env.bot.secret.example`):

```env
TELEGRAM_TOKEN=your_token
LMS_API_BASE_URL=http://localhost:42002
LMS_API_KEY=your_key
LLM_API_BASE_URL=http://localhost:8000
LLM_API_KEY=your_key
```

2. No secrets are committed to git - `.env.bot.secret` is in `.gitignore`.

### Docker Deployment (Task 4)

For docker-compose, use `.env.docker.secret`:

```env
TELEGRAM_TOKEN=your_token
LMS_API_KEY=your_key
LLM_API_KEY=your_key
```

Environment URLs in docker-compose use service names: `http://backend:42002` (not localhost).

## Architecture

See `PLAN.md` for detailed architecture decisions:

- **Task 1**: Handlers as pure functions, testable without Telegram
- **Task 2**: Async HTTP client for LMS API with Bearer auth
- **Task 3**: LLM tool calling - formal tool descriptions (NO regex routing)
- **Task 4**: Docker multi-service deployment with service-name DNS

## Key Design Principles

1. **No hardcoded URLs or API keys** - everything from config
2. **No secrets in git** - .env files are .gitignored
3. **Pure handlers** - easy to test and reuse
4. **Async I/O** - ready for concurrent requests
5. **Tool descriptions matter** - LLM chooses based on quality descriptions

## Development Workflow

1. Modify handlers in `bot/handlers/commands.py`
2. Run `python bot.py --test "/command"` to verify
3. Add tests in `tests/test_*.py`
4. Run `pytest tests/ -v` to validate

## Docker

```bash
# Build and start all services
docker compose up -d --build

# Test bot in container
docker compose exec bot python bot.py --test "/start"

# Check bot can reach backend
docker compose exec bot curl -s http://backend:42002/health

# View logs
docker compose logs bot
```


