
"""End-to-end tests for the chat API using a mocked ADK service."""

import importlib
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure the service's local config module is available as ``config``
sys.modules.setdefault(
    "config", importlib.import_module("services.agent_service.config")
)
sys.modules.setdefault(
    "api", importlib.import_module("services.agent_service.api")
)
sys.modules.setdefault(
    "models", importlib.import_module("services.agent_service.models")
)
sys.modules.setdefault(
    "agents_adk", importlib.import_module("services.agent_service.agents_adk")
)
sys.modules.setdefault(
    "services.adk_chat_service",
    importlib.import_module("services.agent_service.services.adk_chat_service"),
)

from services.agent_service.main import app

class MockADKChatService:
    def __init__(self):
        self.history = {}

    async def send_message(self, user_id: str, text: str, context=None):
        self.history.setdefault(user_id, []).append({"sender": "user", "content_type": "text", "payload": {"text": text}})
        response = {"message": f"Echo: {text}", "metadata": {}, "success": True}
        self.history[user_id].append({"sender": "agent", "content_type": "text", "payload": response})
        return "text", response

    def get_conversation_history(self, user_id: str):
        return self.history.get(user_id, [])

    def clear_conversation_history(self, user_id: str):
        self.history.pop(user_id, None)
        return True

@pytest.fixture
def client(monkeypatch):
    mock_service = MockADKChatService()
    monkeypatch.setattr("services.agent_service.api.chat.adk_chat_service", mock_service)
    monkeypatch.setattr("services.agent_service.services.adk_chat_service.adk_chat_service", mock_service)
    return TestClient(app)


def test_send_chat_and_history_flow(client):
    resp = client.post("/api/chat/send", json={"user_id": "u1", "text": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["content_type"] == "text"
    assert data["payload"]["message"] == "Echo: hello"

    hist_resp = client.get("/api/chat/history", params={"user_id": "u1"})
    assert hist_resp.status_code == 200
    hist = hist_resp.json()
    assert len(hist) == 2
    assert hist[0]["sender"] == "user"
    assert hist[1]["sender"] == "agent"


def test_health_endpoint(client):
    resp = client.get("/api/health/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "agents_available": True}


def test_send_chat_error(client, monkeypatch):
    """The API should return 500 when the chat service raises an error."""
    import services.agent_service.api.chat as chat_mod

    async def boom(user_id: str, text: str, context=None):
        raise RuntimeError("boom")

    monkeypatch.setattr(chat_mod.adk_chat_service, "send_message", boom)

    resp = client.post("/api/chat/send", json={"user_id": "u2", "text": "hi"})
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Failed to process chat request"


def test_clear_history_endpoint(client):
    client.post("/api/chat/send", json={"user_id": "u3", "text": "hi"})
    resp = client.delete("/api/chat/history/u3")
    assert resp.status_code == 200
    assert "cleared" in resp.json()["message"]
    hist = client.get("/api/chat/history", params={"user_id": "u3"}).json()
    assert hist == []
