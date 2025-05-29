from agents.workflow import run_workflow
from app.models import Message


def test_reporting_route():
    state = run_workflow("show me a chart")
    assert state.result["content_type"] == Message.CHART
    assert [step["agent"] for step in state.conversation] == ["orchestrator", "reporting"]


def test_safety_route():
    state = run_workflow("tell me about safety")
    assert state.result["content_type"] == Message.TEXT
    assert [step["agent"] for step in state.conversation] == ["orchestrator", "safety"]


def test_onboarding_then_reporting():
    state = run_workflow("hello")
    assert state.result["content_type"] == Message.CHART
    assert [step["agent"] for step in state.conversation] == [
        "orchestrator",
        "onboarding",
        "reporting",
    ]


def test_other_routes():
    data = [
        ("show me the cash flow", "cash_flow"),
        ("goal planning", "goal_setting"),
        ("tell me about taxes", "tax_pension"),
        ("i want investment advice", "investment"),
    ]
    for text, expected in data:
        state = run_workflow(text)
        assert state.result["content_type"] == Message.TEXT
        assert [step["agent"] for step in state.conversation] == [
            "orchestrator",
            expected,
        ]
