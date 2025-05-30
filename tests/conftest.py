import os
import django
import litellm
import json
import pytest

# ensure required settings for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.test_settings")
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


@pytest.fixture
def orchestrator_llm(monkeypatch):
    """Return a deterministic LLM response for the orchestrator."""
    def _mock_completion(model, messages, **kwargs):
        text = messages[-1]["content"].lower()
        if "upload" in text and "chart" in text:
            agent = "Orchestrator"
            intent = "clarify"
            params = {"question": "Upload or chart first?"}
        elif "joke" in text:
            agent = "Orchestrator"
            intent = "fallback"
            params = {"message": messages[-1]["content"]}
        elif "chart" in text or "graph" in text:
            agent = "Reporting & Visualisation"
            intent = "show_budget"
            params = {}
        elif "safety" in text:
            agent = "Safety-Layer"
            intent = "assess_safety"
            params = {}
        elif "goal" in text:
            agent = "Goal-Setting"
            intent = "set_goal"
            params = {}
        elif "tax" in text:
            agent = "Tax & Pension Optimiser"
            intent = "tax_optimiser"
            params = {}
        elif "invest" in text:
            agent = "Investment Architect"
            intent = "plan_investment"
            params = {}
        elif "cash" in text:
            agent = "Cash-Flow & Budget"
            intent = "categorize_txns"
            params = {}
        elif "debt" in text:
            agent = "Debt-Strategy"
            intent = "debt_strategy"
            params = {}
        else:
            agent = "Onboarding & Baseline"
            intent = "upload_documents"
            params = {}

        response = json.dumps({
            "schema_version": "1",
            "agent": agent,
            "intent": intent,
            "params": params,
        })
        return litellm.mock_completion(model=model, messages=messages, mock_response=response)

    monkeypatch.setattr(litellm, "completion", _mock_completion)
    return _mock_completion
