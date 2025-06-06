"""Unit tests for ADKChatService state management and error handling."""

import asyncio
from datetime import timedelta

from services.agent_service.services import adk_chat_service as service_module
from services.agent_service.tools import finance_data_client

ADKChatService = service_module.ADKChatService


def test_get_conversation_state_caches(monkeypatch):
    """get_conversation_state should load context only once and cache it."""
    calls = []

    class DummyClient:
        def get_conversation_context_sync(self, token):
            calls.append(token)
            return {"context": {"loaded": True}}

    monkeypatch.setattr(finance_data_client, "get_finance_client", lambda: DummyClient())
    monkeypatch.setattr(service_module, "get_finance_client", lambda: DummyClient())

    svc = ADKChatService()
    state1 = svc.get_conversation_state("u1")
    state2 = svc.get_conversation_state("u1")

    assert state1 is state2
    assert state1.get_context()["loaded"] is True
    assert calls == ["u1"]


def test_send_message_handles_exception(monkeypatch):
    """send_message should return an error payload if process_message fails."""
    svc = ADKChatService()

    async def boom(*args, **kwargs):
        raise ValueError("fail")

    monkeypatch.setattr(svc, "process_message", boom)

    async def run():
        return await svc.send_message("u1", "hello")

    content_type, payload = asyncio.run(run())

    assert content_type == "text"
    assert payload["success"] is False
    assert "fail" in payload["error"]


def test_cleanup_expired_sessions(monkeypatch):
    """cleanup_expired_sessions should remove states older than max_age_hours."""
    svc = ADKChatService()

    old_state = svc.get_conversation_state("old")
    new_state = svc.get_conversation_state("new")
    old_state.last_updated -= timedelta(hours=2)

    svc.adk_sessions["old"] = object()
    svc.adk_runners["old"] = object()

    svc.cleanup_expired_sessions(max_age_hours=1)

    assert "old" not in svc.conversation_states
    assert "old" not in svc.adk_sessions
    assert "old" not in svc.adk_runners
    assert "new" in svc.conversation_states
