"""Unit tests for finance_tools verifying parameter handling and client calls."""

import json
from services.agent_service.agents_adk.tools import finance_tools
from google.adk.tools.tool_context import ToolContext


def test_get_user_transactions_parses_filters(monkeypatch):
    """Ensure get_user_transactions parses the date_range and passes parameters to the client."""
    captured = {}

    class DummyClient:
        def get_filtered_transactions_sync(self, token, **kwargs):
            captured['token'] = token
            captured.update(kwargs)
            return [{'id': 1, 'amount': -5, 'description': 'foo'}]

    monkeypatch.setattr(finance_tools, "get_finance_client", lambda: DummyClient())

    ctx = ToolContext()
    ctx.state = {'user_token': 'tok'}
    result = finance_tools.get_user_transactions(ctx, date_range="2025-04", category="food", limit=5)
    data = json.loads(result)

    assert data['transactions'] == [{'id': 1, 'amount': -5, 'description': 'foo'}]
    assert captured['category'] == 'food'
    assert captured['start_date'] == '2025-04-01'
    assert captured['end_date'] == '2025-04-30'
    assert captured['limit'] == 5


def test_generate_financial_report_context(monkeypatch):
    """generate_financial_report should return context via the client."""
    class DummyClient:
        def get_financial_context_sync(self, token, **kwargs):
            return {'dummy': True}

    monkeypatch.setattr(finance_tools, "get_finance_client", lambda: DummyClient())

    ctx = ToolContext()
    ctx.state = {'token': 'tok'}
    result = finance_tools.generate_financial_report(ctx, report_type="financial_context")
    data = json.loads(result)

    assert data['report_type'] == 'financial_context'
    assert data['context'] == {'dummy': True}


def test_generate_financial_report_error(monkeypatch):
    """generate_financial_report should surface client errors."""
    class DummyClient:
        def get_budget_analysis_sync(self, token, period="month"):
            raise RuntimeError("boom")
    monkeypatch.setattr(finance_tools, "get_finance_client", lambda: DummyClient())
    ctx = ToolContext()
    ctx.state = {"user_token": "tok"}
    result = finance_tools.generate_financial_report(ctx, report_type="budget_analysis")
    data = json.loads(result)
    assert data["error"].startswith("Failed to generate report")
