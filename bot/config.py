"""Configuration management for the LMS bot.

Loads environment variables from .env.bot.secret file.
"""

from pathlib import Path
import os


class BotSettings:
    """Bot configuration from environment variables.
    
    All secrets are loaded from .env.bot.secret file, which is .gitignored.
    """

    def __init__(self, env_file: str = ".env.bot.secret"):
        """Initialize from env file or environment."""
        # Load from .env file if it exists
        if Path(env_file).exists():
            self._load_env_file(env_file)
        
        # Read environment variables
        self.bot_token = os.getenv("BOT_TOKEN", "")
        self.telegram_token = self.bot_token  # Alias
        self.lms_api_base_url = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
        self.lms_api_key = os.getenv("LMS_API_KEY", "my-secret-api-key")
        self.llm_api_base_url = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
        self.llm_api_key = os.getenv("LLM_API_KEY", "default-key")
        self.llm_api_model = os.getenv("LLM_API_MODEL", "coder-model")

        # Validate required fields
        if not self.bot_token:
            raise ValueError("BOT_TOKEN is required in .env.bot.secret")
    
    def _load_env_file(self, path: str) -> None:
        """Load environment variables from .env file (simple parser, no external deps)."""
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Could not load env file {path}: {e}")


def load_config(env_file=None):
    """Load bot configuration from environment file.
    
    Searches in: current dir, parent dir, and /root/se-toolkit-lab-7
    
    Args:
        env_file: Optional path to .env file. Defaults to .env.bot.secret.
        
    Returns:
        BotSettings instance with validated configuration.
    """
    # Try multiple locations
    search_paths = [
        Path(env_file or ".env.bot.secret"),
        Path("..") / (env_file or ".env.bot.secret"),
        Path("/root/se-toolkit-lab-7") / (env_file or ".env.bot.secret"),
    ]
    
    for env_path in search_paths:
        if env_path.exists():
            return BotSettings(str(env_path))
    
    # Fallback: try to load from environment or use defaults
    return BotSettings(env_file or ".env.bot.secret")


# Export a global config instance for easy import
# Only load if env file exists, otherwise lazy load
_config = None

def get_config():
    """Lazy load config on first access."""
    global _config
    if _config is None:
        _config = load_config()
    return _config

# For backwards compatibility - access via get_config()
config = None  # Will be set on first use
