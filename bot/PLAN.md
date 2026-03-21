# Bot Implementation Plan

## Architecture Overview

This bot follows a layered architecture with clear separation of concerns:

- **Entry Point** (`bot.py`): Command parsing and routing
- **Handlers** (`handlers/`): Pure functions for command logic
- **Services** (`services/`): External API clients (LMS, LLM)
- **Config** (`config.py`): Environment variable loading

## Design Decisions

### 1. Handler Separation (Task 1)
- Handlers are pure functions that take input and return text.
- No direct dependency on Telegram API → easily testable.
- Same handler can be invoked from `--test` mode, unit tests, or real Telegram updates.

**Pattern**: Separation of concerns - business logic separate from I/O layer.

### 2. Configuration Management (Task 2)
- All secrets (tokens, API keys) loaded from `.env.bot.secret` file.
- `.env.bot.secret` is `.gitignored` - secrets never committed.
- Uses `pydantic-settings` for type-safe environment loading.

**Why**: Prevents accidental secret leaks and enables different configs per environment.

### 3. API Client (Task 2)
- `LMSClient` provides async HTTP methods for backend communication.
- Uses `httpx` instead of `requests` - supports async/await patterns.
- Bearer token authentication in headers.
- Base URLs and keys from config, never hardcoded.

**Why**: Async enables efficient concurrent requests; Bearer auth is LMS standard.

### 4. LLM Tool Calling (Task 3)
- `LLMClient` defines tools as `ToolDefinition` objects with formal descriptions.
- Tools have name, description, and JSON schema for parameters.
- LLM reads tool descriptions to decide which to invoke.
- **NO regex or keyword matching** - description quality is key.

**Pattern**: Function calling / Tool use - follows OpenAI and Anthropic standards.

**Why this design**: 
- If LLM chooses wrong tool → improve description, not code logic.
- If you hardcode keyword → not learning LLM's actual capabilities.
- Real LLM services use this exact pattern.

### 5. Docker Deployment (Task 4)
- Bot service in `docker-compose.yml` depends on backend service.
- Uses service name `backend` instead of `localhost` for internal DNS.
- All external URLs from config (environment variables in docker-compose).

**Why**: Services on same network find each other by service name; localhost is container's own loopback.

## File Structure

```
bot/
├── bot.py                 # Entry point, command parsing/routing
├── config.py              # Environment loading (pydantic-settings)
├── handlers/
│   ├── __init__.py       # Exports handlers
│   └── commands.py       # Pure handler functions
├── services/
│   ├── __init__.py
│   ├── lms_client.py     # Task 2: HTTP client for LMS backend
│   └── llm_client.py     # Task 3: LLM tool calling interface
├── pyproject.toml        # Dependencies (uv-managed)
├── Dockerfile            # Task 4: Container image
└── PLAN.md              # This file
```

## Tasks and Implementation

### Task 1: Basic Bot and Test Mode
- ✅ Create `bot.py` with `--test` flag
- ✅ Create `handlers/commands.py` with pure functions
- ✅ Route commands: `/start`, `/help`, `/health`, `/labs`, `/scores`
- ✅ Test: `python bot.py --test "/start"`

### Task 2: Configuration and API Client
- ✅ Create `config.py` with `pydantic-settings`
- ✅ Create `services/lms_client.py` with async HTTP methods
- ✅ Methods: `get_items()`, `get_labs()`, `get_scores(user_id)`
- ✅ Authentication: Bearer token from config
- ✅ No hardcoded URLs or keys

### Task 3: LLM Tool Calling
- ✅ Create `services/llm_client.py` with `ToolDefinition`
- ✅ Define tools: `get_labs`, `get_scores`
- ✅ Each tool has: name, description, input_schema
- ✅ Method: `ask_llm(prompt)` returns tool choice and reasoning
- ❌ NO regex routing - LLM chooses based on descriptions

### Task 4: Docker and Networking
- ✅ Create `bot/Dockerfile`
- ✅ Update `docker-compose.yml` with bot service
- ✅ Bot uses service name `backend:8000` for internal DNS
- ✅ Environment variables from `.env.docker.secret`

## Testing Strategy

### Unit Tests
- `tests/test_handlers.py`: Test pure handler functions
- `tests/test_lms_client.py`: Mock HTTP responses, test client logic
- `tests/test_llm_client.py`: Test tool definition and LLM interface

### Integration Tests
- `tests/test_bot_routing.py`: Test command parsing and routing
- Manual test: `python bot.py --test "/command"`

### Docker Tests
- `docker compose up -d`
- `docker compose exec bot python bot.py --test "/start"`
- `docker compose exec bot curl http://backend:8000/health`

## Key Takeaways

1. **Handlers are testable**: Pure functions, no side effects, easy to unit test.
2. **Config is centralized**: All secrets and URLs in one place, never hardcoded.
3. **Services are async**: Uses `httpx` for efficient I/O, ready for concurrent requests.
4. **LLM tool descriptions are critical**: Good descriptions = better routing, no regex hacks.
5. **Docker uses service names**: `backend:8000` works because they're on same network.

