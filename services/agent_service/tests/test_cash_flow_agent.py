import pytest
from agents.cash_flow import CashFlowAgent
from app.models import Message


def test_create_budget_requires_fields():
    agent = CashFlowAgent()
    content_type, payload = agent.handle_message(
        "create my budget",
        intent="create_budget",
        budget_info={},
    )
    assert content_type == Message.TEXT
    assert "missing_info" in payload
    assert "net_income" in payload["missing_info"]
