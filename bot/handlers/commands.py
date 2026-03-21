"""Command handlers for basic bot functionality.

These handlers are pure functions with no dependencies on Telegram API.
Pattern: Separation of concerns - handlers separate from I/O layer.
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


def handle_labs() -> str:
    """Handle /labs command (placeholder for task-2).
    
    In task-2, this will fetch actual labs from LMS API.
    
    Returns:
        Placeholder message.
    """
    return "Labs: [fetching from LMS... will be implemented in task-2]"


def handle_scores() -> str:
    """Handle /scores command (placeholder for task-2).
    
    In task-2, this will fetch actual scores from LMS API.
    
    Returns:
        Placeholder message.
    """
    return "Scores: [fetching from LMS... will be implemented in task-2]"
