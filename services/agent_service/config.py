"""Configuration for agent service."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the service root directory
SERVICE_ROOT = Path(__file__).parent.absolute()
ENV_FILE = SERVICE_ROOT / '.env'

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Helper function to get config values with defaults
def config(key: str, default=None, cast=None):
    value = os.environ.get(key)
    if value is None:
        return default
    if cast and value is not None:
        if cast == bool:
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes', 'on')
        return cast(value)
    return value

# Database configuration
DATABASE_URL = config('DATABASE_URL', default='postgresql://finance_user:finance_password@localhost:5432/finance')

# Core API configuration
CORE_API_URL = config('CORE_API_URL', default='http://localhost:8000')

# Agent configuration
AGENT_DEBUG = config('AGENT_DEBUG', default=True, cast=bool)
AGENT_LOG_LEVEL = config('AGENT_LOG_LEVEL', default='INFO')

# LLM configuration
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')

# Google AI configuration
GOOGLE_API_KEY = config('GOOGLE_API_KEY', default='')
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
GOOGLE_GENAI_USE_VERTEXAI = config('GOOGLE_GENAI_USE_VERTEXAI', default=False, cast=bool)
GOOGLE_CLOUD_PROJECT = config('GOOGLE_CLOUD_PROJECT', default='')
GOOGLE_CLOUD_LOCATION = config('GOOGLE_CLOUD_LOCATION', default='us-central1')

# ADK configuration
ADK_PROJECT_ID = config('ADK_PROJECT_ID', default='')
ADK_REGION = config('ADK_REGION', default='us-central1')

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 