"""Configuration management for the LMS bot.

Loads environment variables from .env.bot.secret file.
Uses pydantic-settings for validation and type safety.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    """Bot configuration from environment variables.
    
    All secrets are loaded from .env.bot.secret file, which is .gitignored.
    Field names should match environment variables (case-insensitive).
    """

    bot_token: str  # BOT_TOKEN from .env
    lms_api_base_url: str
    lms_api_key: str
    llm_api_base_url: str = "http://localhost:42005/v1"
    llm_api_key: str = "default-key"
    llm_api_model: str = "coder-model"

    # Alias for convenience
    @property
    def telegram_token(self) -> str:
        """Alias for bot_token for backwards compatibility."""
        return self.bot_token

    class Config:
        """Pydantic config."""
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env


def load_config(env_file: str | None = None) -> BotSettings:
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
    
    return BotSettings(_env_file=env_file or ".env.bot.secret")
