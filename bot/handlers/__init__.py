"""Bot command handlers module.

Handlers are pure functions that take input and return text.
They don't depend on Telegram API, making them testable and reusable.

Organized into submodules:
- basic: Core commands (/start, /help, /health)
- lms: LMS integration commands (/labs, /scores)
"""

from bot.handlers.basic import (
    handle_health,
    handle_help,
    handle_start,
)
from bot.handlers.lms import (
    handle_labs,
    handle_scores,
)

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
]
