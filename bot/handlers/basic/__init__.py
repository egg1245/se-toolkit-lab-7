"""Basic command handlers for the LMS bot.

These are pure functions with no dependencies on Telegram API.
They implement core bot commands: /start, /help, /health.
"""


def handle_start() -> str:
    """Handle /start command.
    
    Returns:
        Welcome message.
    """
    return (
        "Welcome to LMS Bot! 👋\n\n"
        "I can help you with lab submissions, grades, and course information.\n"
        "Use /help to see all available commands."
    )


def handle_help() -> str:
    """Handle /help command.
    
    Returns:
        List of available commands with descriptions.
    """
    commands = [
        ("/start", "Show welcome message"),
        ("/help", "Show this help message"),
        ("/health", "Check bot status"),
        ("/labs", "List available labs"),
        ("/scores", "Show your current scores"),
    ]
    
    help_text = "Available commands:\n\n"
    for cmd, desc in commands:
        help_text += f"{cmd} - {desc}\n"
    
    return help_text


def handle_health() -> str:
    """Handle /health command.
    
    Returns:
        Health status message.
    """
    return "Bot is running and healthy ✓"
