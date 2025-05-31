"""
Integration Test Configuration

This conftest.py is completely independent from the unit test configuration.
It sets up Django for integration tests without any mocking or interference
from the unit test infrastructure.
"""

import os
import sys
import django
import pytest

# Add the project root to Python path so we can import the app modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Django settings for integration tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.test_settings")

# Set required environment variables for Django
for var in [
    "GRID_ENDPOINT",
    "FRONT_ENDPOINT", 
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "HOST",
    "REDIS_ENDPOINT",
]:
    os.environ.setdefault(var, "test")

# Initialize Django
django.setup()

# NOTE: No autouse fixtures that mock litellm or any other components
# Integration tests should use real services and make real API calls 