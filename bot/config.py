"""Configuration management for the LMS bot.

Loads environment variables from .env.bot.secret file.
"""

from pathlib import Path
import os
from dotenv import load_dotenv


class BotSettings:
    """Bot configuration from environment variables.
    
    All secrets are loaded from .env.bot.secret file, which is .gitignored.
    """

    def __init__(self, env_file: str = ".env.bot.secret"):
        """Initialize from env file or environment."""
        # Load from .env file if it exists
        if Path(env_file).exists():
            load_dotenv(env_file)
        
        # Read environment variables
        self.bot_token = os.getenv("BOT_TOKEN", "")
        self.telegram_token = self.bot_token  # Alias
        self.lms_api_base_url = os.getenv("LMS_API_BASE_URL", "http://localhost:42011")
        self.lms_api_key = os.getenv("LMS_API_KEY", "my-secret-api-key")
        self.llm_api_base_url = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
        self.llm_api_key = os.getenv("LLM_API_KEY", "default-key")
        self.llm_api_model = os.getenv("LLM_API_MODEL", "coder-model")

        # Validate required fields
        if not self.bot_token:
            raise ValueError("BOT_TOKEN is required in .env.bot.secret")


def load_config(env_file=None):
    """Load bot configuration from environment file.
    
    Args:
        env_file: Optional path to .env file. Defaults to .env.bot.secret.
        
    Returns:
        BotSettings instance with validated configuration.
        
    Raises:
        FileNotFoundError: If env_file doesn't exist.
        ValueError: If required settings are missing or invalid.
    """
    if env_file:
        env_path = Path(env_file)
        if not env_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {env_path}")
    
    return BotSettings(env_file or ".env.bot.secret")
