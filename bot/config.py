"""Configuration management for the LMS bot.

Loads environment variables from .env.bot.secret file.
Uses pydantic-settings for validation and type safety.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    """Bot configuration from environment variables.
    
    All secrets are loaded from .env.bot.secret file, which is .gitignored.
    Field names should match environment variables (case-insensitive).
    """

    bot_token: str = Field(alias="BOT_TOKEN")
    lms_api_base_url: str = Field(alias="LMS_API_BASE_URL")
    lms_api_key: str = Field(alias="LMS_API_KEY")
    llm_api_base_url: str = Field(default="http://localhost:42005/v1", alias="LLM_API_BASE_URL")
    llm_api_key: str = Field(default="default-key", alias="LLM_API_KEY")
    llm_api_model: str = Field(default="coder-model", alias="LLM_API_MODEL")

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
        populate_by_name = True  # Allow both field name and alias


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
