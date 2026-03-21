"""DEPRECATED: This file is kept for backward compatibility.

This module is deprecated. All command handlers have moved to:
  bot.handlers.basic - Core commands
  bot.handlers.lms - LMS integration commands

Import from bot.handlers instead:
  from bot.handlers import handle_start, handle_help, etc.
"""

# Backward compatibility re-exports
from bot.handlers import (
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
