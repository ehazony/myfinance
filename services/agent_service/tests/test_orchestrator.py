import pytest
from agents.orchestrator import Orchestrator
from app.models import Message


def test_route_with_llm(orchestrator_llm):
    orch = Orchestrator()
    assert orch.route("show me a chart") == "reporting"


def test_fallback_to_heuristics():
    orch = Orchestrator()
    assert orch.route("show me a chart") == "reporting"


def test_handle_message_special_intents(orchestrator_llm):
    orch = Orchestrator()
    content_type, payload = orch.handle_message("tell me a joke")
    assert content_type == Message.TEXT
    assert payload["text"].lower().startswith("tell me a joke")
