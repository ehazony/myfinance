from agents.conversation import ConversationAgent
from app.models import Message


def test_conversation_agent_summarises():
    agent = ConversationAgent()
    content_type, payload = agent.handle_message(
        "",
        source="Data",
        agent="onboarding",
        payload={"missing_info": ["bank", "credit"]},
    )
    assert content_type == Message.TEXT
    assert "missing" in payload["messages"][0]

