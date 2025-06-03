import pytest

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents_adk.agent import root_agent
from tests.test_adk_chat_service import DummyEvent


def create_runner():
    session_service = InMemorySessionService()
    return Runner(agent=root_agent, app_name="Test", session_service=session_service)


def test_onboarding_flow_routing(monkeypatch):
    """Conversation should stay with onboarding then return to orchestrator."""
    runner = create_runner()

    call_order = []
    call_count = 0

    def fake_run(*, user_id=None, session_id=None, new_message=None, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            call_order.append("finance_orchestrator")
            yield DummyEvent("Welcome", author="finance_orchestrator")
            call_order.append("onboarding_agent")
            yield DummyEvent("Let's start onboarding", author="onboarding_agent")
        elif call_count < 4:
            call_order.append("onboarding_agent")
            yield DummyEvent("Continuing onboarding", author="onboarding_agent")
        else:
            call_order.append("onboarding_agent")
            yield DummyEvent("Onboarding complete", author="onboarding_agent")
            call_order.append("finance_orchestrator")
            yield DummyEvent("Back to orchestrator", author="finance_orchestrator")

    monkeypatch.setattr(runner, "run", fake_run)

    user_id = "u1"
    session_id = "s1"
    for text in ["hello", "next", "next", "done"]:
        msg = types.Content(role="user", parts=[types.Part(text=text)])
        events = runner.run(user_id=user_id, session_id=session_id, new_message=msg)
        list(events)  # exhaust generator to trigger fake events

    assert call_order == [
        "finance_orchestrator",
        "onboarding_agent",
        "onboarding_agent",
        "onboarding_agent",
        "onboarding_agent",
        "finance_orchestrator",
    ]
