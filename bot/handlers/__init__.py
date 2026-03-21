"""Bot command handlers module.

Handlers are pure functions that take input and return text.
They don't depend on Telegram API, making them testable and reusable.
"""

from bot.handlers.commands import (
    handle_health,
    handle_help,
    handle_labs,
    handle_scores,
    handle_start,
)

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
]
