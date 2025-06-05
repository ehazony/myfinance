"""Configuration for telegram bot service."""

import os
from decouple import config

# Database configuration
DATABASE_URL = config('DATABASE_URL', default='postgresql://finance_user:finance_password@localhost:5432/finance')

# Core API configuration
CORE_API_URL = config('CORE_API_URL', default='http://localhost:8000')

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_BOT_USERNAME = config('TELEGRAM_BOT_USERNAME', default='FinanceBot')

# Bot behavior configuration
BOT_DEBUG = config('BOT_DEBUG', default=True, cast=bool)
BOT_LOG_LEVEL = config('BOT_LOG_LEVEL', default='INFO')
MAX_MESSAGE_LENGTH = config('MAX_MESSAGE_LENGTH', default=4096, cast=int)

# Conversation settings
CONVERSATION_TIMEOUT = config('CONVERSATION_TIMEOUT', default=3600, cast=int)  # 1 hour
MAX_CONVERSATIONS_PER_USER = config('MAX_CONVERSATIONS_PER_USER', default=10, cast=int)

# Rate limiting
RATE_LIMIT_MESSAGES = config('RATE_LIMIT_MESSAGES', default=10, cast=int)
RATE_LIMIT_WINDOW = config('RATE_LIMIT_WINDOW', default=60, cast=int)  # seconds

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 