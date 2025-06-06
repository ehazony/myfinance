"""Unit tests for the cash flow agent creation."""

from services.agent_service.agents_adk.agents.cash_flow import create_cash_flow_agent


def test_create_cash_flow_agent():
    agent = create_cash_flow_agent()
    assert agent.kwargs["name"] == "cash_flow_agent"
    assert isinstance(agent.kwargs["tools"], list)
