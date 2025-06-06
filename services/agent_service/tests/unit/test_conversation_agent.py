"""Unit tests for the conversation agent creation."""

from services.agent_service.agents_adk.agents.conversation import (
    create_conversation_agent,
)


def test_create_conversation_agent():
    agent = create_conversation_agent()
    assert agent.kwargs["name"] == "conversation_agent"
    assert isinstance(agent.kwargs["tools"], list)
