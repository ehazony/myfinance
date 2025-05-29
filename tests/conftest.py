import os
import django
import litellm
import pytest

# ensure required settings for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
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

django.setup()

@pytest.fixture(autouse=True)
def mock_litellm(monkeypatch):
    """Mock litellm.completion to avoid network calls."""
    def _mock_completion(model, messages, **kwargs):
        return litellm.mock_completion(model=model, messages=messages, mock_response="{\"ok\": true}")

    monkeypatch.setattr(litellm, "completion", _mock_completion)
    # Skip JSON schema validation during tests
    from agents.base import BaseAgent
    monkeypatch.setattr(BaseAgent, "validate_payload", lambda self, payload: None)
    return _mock_completion
