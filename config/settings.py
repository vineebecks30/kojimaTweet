"""Configuration settings for KojimaTweet application."""
import os
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    # Twitter API Configuration
    twitter_bearer_token: str = Field(..., env="TWITTER_BEARER_TOKEN")
    twitter_username: str = Field(
        default="HIDEO_KOJIMA_EN",
        env="TWITTER_USERNAME"
    )
    
    # API Settings
    max_tweets: int = Field(default=50, env="MAX_TWEETS", ge=1, le=100)
    api_timeout: int = Field(default=30, env="API_TIMEOUT", ge=5, le=120)
    
    # Rating Thresholds
    rating_5_stars: int = Field(default=200, env="RATING_5_STARS", ge=0)
    rating_4_stars: int = Field(default=100, env="RATING_4_STARS", ge=0)
    rating_3_stars: int = Field(default=50, env="RATING_3_STARS", ge=0)
    
    # Caching Configuration
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL", ge=60)
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/kojima_tweet.log", env="LOG_FILE")
    
    # Rate Limiting
    rate_limit_calls: int = Field(default=15, env="RATE_LIMIT_CALLS", ge=1)
    rate_limit_period: int = Field(default=900, env="RATE_LIMIT_PERIOD", ge=60)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
    
    @validator("twitter_bearer_token")
    def validate_bearer_token(cls, v: str) -> str:
        """Validate bearer token is not empty or placeholder."""
        if not v or v == "your_bearer_token_here":
            raise ValueError(
                "TWITTER_BEARER_TOKEN must be set to a valid token. "
                "Copy .env.example to .env and add your credentials."
            )
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v_upper
    
    @validator("rating_5_stars", "rating_4_stars", "rating_3_stars")
    def validate_rating_thresholds(cls, v: int, values: dict) -> int:
        """Validate rating thresholds are in descending order."""
        # This validator runs for each field, so we check what we can
        if "rating_5_stars" in values and "rating_4_stars" in values:
            if values["rating_5_stars"] <= values["rating_4_stars"]:
                raise ValueError(
                    "RATING_5_STARS must be greater than RATING_4_STARS"
                )
        if "rating_4_stars" in values and "rating_3_stars" in values:
            if values["rating_4_stars"] <= values["rating_3_stars"]:
                raise ValueError(
                    "RATING_4_STARS must be greater than RATING_3_STARS"
                )
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
        
    Raises:
        ValueError: If required environment variables are missing or invalid
    """
    try:
        return Settings()
    except Exception as e:
        raise ValueError(
            f"Failed to load settings: {e}\n"
            "Please ensure .env file exists with valid configuration. "
            "See .env.example for reference."
        ) from e


def validate_environment() -> tuple[bool, Optional[str]]:
    """
    Validate environment configuration without raising exceptions.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        get_settings()
        return True, None
    except Exception as e:
        return False, str(e)

# Made with Bob
