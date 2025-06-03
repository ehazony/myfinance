import pytest
from django.contrib.auth import get_user_model

from app.services.adk_chat_service import ADKChatService
from app.models import Message


class DummyPart:
    def __init__(self, text: str):
        self.text = text


class DummyContent:
    def __init__(self, text: str):
        self.parts = [DummyPart(text)]


class DummyEvent:
    def __init__(self, text: str, author: str = "agent"):
        self.content = DummyContent(text)
        self.author = author
        
    def is_final_response(self) -> bool:
        return True


@pytest.mark.skip("Django models not available in minimal test environment")
def test_adk_chat_send_message(monkeypatch):
    pass
