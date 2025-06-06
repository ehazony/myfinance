"""Unit tests for ConversationState helpers and edge cases."""

from services.agent_service.agents_adk.state.conversation_state import ConversationState


def test_from_dict_with_invalid_dates():
    data = {
        "user_id": "u1",
        "context": {"foo": "bar"},
        "messages": [],
        "created_at": "bad",
        "last_updated": "also-bad",
    }
    state = ConversationState.from_dict(data)
    assert state.user_id == "u1"
    assert state.context == {"foo": "bar"}
    assert state.get_message_count() == 0
    # Invalid dates should not raise errors and are ignored
    assert isinstance(state.created_at, type(state.last_updated))
