from agents.workflow import run_workflow
from app.models import Message


def test_full_workflow():
    state = run_workflow("I want to sign up and then see a chart")
    assert state.result["content_type"] == Message.TEXT
    assert state.conversation[-1]["agent"] == "conversation"
