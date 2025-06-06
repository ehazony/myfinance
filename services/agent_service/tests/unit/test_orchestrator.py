"""Unit tests for the finance orchestrator creation."""

from services.agent_service.agents_adk.agents.orchestrator import (
    create_finance_orchestrator,
)


def test_create_finance_orchestrator():
    agent = create_finance_orchestrator()
    assert agent.kwargs["name"] == "finance_orchestrator"
    assert isinstance(agent.kwargs["instruction"], str)
