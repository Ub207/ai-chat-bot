"""
Application configuration module for Todo App Chatbot Phase III.

This module handles environment variable loading, validation, and configuration
for the application. It ensures all required environment variables are present
and provides helpful error messages if they are missing.
"""

import os
import logging
from typing import Optional
try:
    from pydantic import BaseSettings, validator
    # Using Pydantic v1 syntax
    FIELD_VALIDATOR = "validator"
except ImportError:
    # For Pydantic v2, BaseSettings moved to pydantic-settings
    from pydantic_settings import BaseSettings
    from pydantic import field_validator
    FIELD_VALIDATOR = "field_validator"

# Configure logger
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = ""

    # Authentication
    jwt_secret_key: str = ""
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # OpenAI Configuration
    openai_api_key: str = ""

    # Better Auth Configuration
    better_auth_secret: str = ""
    better_auth_url: str = "http://localhost:3000"

    # Application Settings
    app_env: str = "development"
    log_level: str = "info"

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # MCP Configuration
    mcp_server_url: str = "http://localhost:8000"

    # Security
    csrf_secret_key: str = ""

    # CORS Configuration
    frontend_origin: str = ""
    vercel_url: str = ""
    allowed_origins: str = ""

    if FIELD_VALIDATOR == "validator":
        # Pydantic v1 syntax
        @validator('database_url')
        def validate_database_url(cls, v):
            if not v:
                raise ValueError(
                    "DATABASE_URL environment variable is required. "
                    "Please set it in your .env file. "
                    "Example: postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
                )
            if not v.startswith(('postgresql://', 'postgres://', 'sqlite:///')):
                raise ValueError(
                    f"DATABASE_URL must be a valid PostgreSQL or SQLite URL, got: {v[:50]}..."
                )
            return v

        @validator('jwt_secret_key')
        def validate_jwt_secret_key(cls, v):
            if not v:
                raise ValueError(
                    "JWT_SECRET_KEY environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY should be at least 32 characters long for security."
                )
            return v

        @validator('openai_api_key')
        def validate_openai_api_key(cls, v):
            if not v:
                # For Hugging Face Spaces, we allow empty API key as fallback
                # The application should work without OpenAI for core functionality
                return v
            if v and not v.startswith('sk-'):
                raise ValueError(
                    "OPENAI_API_KEY should start with 'sk-' prefix."
                )
            return v

        @validator('better_auth_secret')
        def validate_better_auth_secret(cls, v):
            if not v:
                raise ValueError(
                    "BETTER_AUTH_SECRET environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "BETTER_AUTH_SECRET should be at least 32 characters long for security."
                )
            return v

        @validator('csrf_secret_key')
        def validate_csrf_secret_key(cls, v):
            if not v:
                raise ValueError(
                    "CSRF_SECRET_KEY environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "CSRF_SECRET_KEY should be at least 32 characters long for security."
                )
            return v
    else:
        # Pydantic v2 syntax
        @field_validator('database_url')
        @classmethod
        def validate_database_url(cls, v):
            if not v:
                raise ValueError(
                    "DATABASE_URL environment variable is required. "
                    "Please set it in your .env file. "
                    "Example: postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
                )
            if not v.startswith(('postgresql://', 'postgres://', 'sqlite:///')):
                raise ValueError(
                    f"DATABASE_URL must be a valid PostgreSQL or SQLite URL, got: {v[:50]}..."
                )
            return v

        @field_validator('jwt_secret_key')
        @classmethod
        def validate_jwt_secret_key(cls, v):
            if not v:
                raise ValueError(
                    "JWT_SECRET_KEY environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY should be at least 32 characters long for security."
                )
            return v

        @field_validator('openai_api_key')
        @classmethod
        def validate_openai_api_key(cls, v):
            if not v:
                # For Hugging Face Spaces, we allow empty API key as fallback
                # The application should work without OpenAI for core functionality
                return v
            if v and not v.startswith('sk-') and not v.startswith('sk-test-placeholder'):
                # Allow the placeholder key for development
                raise ValueError(
                    "OPENAI_API_KEY should start with 'sk-' prefix."
                )
            return v

        @field_validator('better_auth_secret')
        @classmethod
        def validate_better_auth_secret(cls, v):
            if not v:
                raise ValueError(
                    "BETTER_AUTH_SECRET environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "BETTER_AUTH_SECRET should be at least 32 characters long for security."
                )
            return v

        @field_validator('csrf_secret_key')
        @classmethod
        def validate_csrf_secret_key(cls, v):
            if not v:
                raise ValueError(
                    "CSRF_SECRET_KEY environment variable is required. "
                    "Please set it in your .env file. "
                    "It should be a long, random string for security."
                )
            if len(v) < 32:
                raise ValueError(
                    "CSRF_SECRET_KEY should be at least 32 characters long for security."
                )
            return v

    model_config = {"env_file": ".env", "case_sensitive": True}

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env.lower() == "development"

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"


# Create a global instance of settings
settings = Settings()


def validate_environment() -> None:
    """
    Validate all environment variables and provide helpful error messages.

    This function checks that all required environment variables are present
    and properly formatted. It raises exceptions with clear instructions
    if any issues are found.
    """
    try:
        # Validate database URL
        if not settings.database_url:
            raise ValueError(
                "Missing DATABASE_URL environment variable. "
                "Please create a .env file in the backend directory with a valid PostgreSQL URL."
            )

        # Validate JWT secret key
        if not settings.jwt_secret_key:
            raise ValueError(
                "Missing JWT_SECRET_KEY environment variable. "
                "Please create a .env file in the backend directory with a secure JWT secret."
            )

        # Validate OpenAI API key
        if not settings.openai_api_key:
            raise ValueError(
                "Missing OPENAI_API_KEY environment variable. "
                "Please create a .env file in the backend directory with your OpenAI API key."
            )

        # Validate Better Auth secret
        if not settings.better_auth_secret:
            raise ValueError(
                "Missing BETTER_AUTH_SECRET environment variable. "
                "Please create a .env file in the backend directory with a secure auth secret."
            )

        # Validate CSRF secret key
        if not settings.csrf_secret_key:
            raise ValueError(
                "Missing CSRF_SECRET_KEY environment variable. "
                "Please create a .env file in the backend directory with a secure CSRF secret."
            )

        logger.info("All required environment variables are present and valid.")

    except ValueError as e:
        logger.error(f"Environment validation failed: {str(e)}")
        logger.info("To fix this issue:")
        logger.info("1. Create a .env file in the backend directory")
        logger.info("2. Copy the contents from .env.example")
        logger.info("3. Replace the placeholder values with your actual values")
        logger.info("4. Make sure all required variables are present")
        raise


def get_database_url() -> str:
    """Get the database URL from settings."""
    return settings.database_url


def get_openai_api_key() -> str:
    """Get the OpenAI API key from settings."""
    return settings.openai_api_key


def get_jwt_secret_key() -> str:
    """Get the JWT secret key from settings."""
    return settings.jwt_secret_key


def get_auth_settings() -> dict:
    """Get authentication-related settings."""
    return {
        "secret_key": settings.jwt_secret_key,
        "algorithm": "HS256",
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "refresh_token_expire_days": settings.refresh_token_expire_days,
    }


if __name__ == "__main__":
    # Validate environment when module is run directly
    validate_environment()
    logger.info("Environment configuration is valid and ready for use.")