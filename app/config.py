"""Application configuration using environment variables."""

import os
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.supabase_url: str = os.getenv("SUPABASE_URL", "")
        self.supabase_key: str = os.getenv("SUPABASE_KEY", "")
        self.supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")
        self.secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    def validate(self) -> None:
        """Validate required settings are present."""
        if not self.supabase_url:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not self.supabase_key:
            raise ValueError("SUPABASE_KEY environment variable is required")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

