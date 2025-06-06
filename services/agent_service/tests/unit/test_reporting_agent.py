"""Unit tests for the reporting agent creation."""

from services.agent_service.agents_adk.agent import create_reporting_agent


def test_create_reporting_agent():
    agent = create_reporting_agent()
    assert agent.kwargs["name"] == "reporting_agent"
    assert "financial" in agent.kwargs["description"].lower()
