"""Configuration for scraper service."""

import os
from decouple import config

# Database configuration
DATABASE_URL = config('DATABASE_URL', default='postgresql://finance_user:finance_password@localhost:5432/finance')

# Core API configuration
CORE_API_URL = config('CORE_API_URL', default='http://localhost:8000')

# Scraper configuration
SCRAPER_DEBUG = config('SCRAPER_DEBUG', default=True, cast=bool)
SCRAPER_LOG_LEVEL = config('SCRAPER_LOG_LEVEL', default='INFO')

# Chrome/Selenium configuration
CHROME_BIN = config('CHROME_BIN', default='/usr/bin/google-chrome')
CHROME_DRIVER_PATH = config('CHROME_DRIVER_PATH', default='')
HEADLESS_MODE = config('HEADLESS_MODE', default=True, cast=bool)

# Timeouts and delays
PAGE_LOAD_TIMEOUT = config('PAGE_LOAD_TIMEOUT', default=30, cast=int)
ELEMENT_WAIT_TIMEOUT = config('ELEMENT_WAIT_TIMEOUT', default=10, cast=int)
SCRAPE_DELAY = config('SCRAPE_DELAY', default=2, cast=int)

# Security
MAX_RETRY_ATTEMPTS = config('MAX_RETRY_ATTEMPTS', default=3, cast=int)
RATE_LIMIT_DELAY = config('RATE_LIMIT_DELAY', default=5, cast=int)

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 