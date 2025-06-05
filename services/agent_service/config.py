"""Configuration for agent service."""

import os
from pathlib import Path
from decouple import config, Config

# Get the service root directory
SERVICE_ROOT = Path(__file__).parent.absolute()
ENV_FILE = SERVICE_ROOT / '.env'

# Initialize config with explicit .env file path
git config = Config(str(ENV_FILE))

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

# ADK configuration
ADK_PROJECT_ID = config('ADK_PROJECT_ID', default='')
ADK_REGION = config('ADK_REGION', default='us-central1')

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 