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
    def __init__(self, text: str):
        self.content = DummyContent(text)

    def is_final_response(self) -> bool:
        return True


@pytest.mark.django_db
def test_adk_chat_send_message(monkeypatch):
    user = get_user_model().objects.create_user(username="tester_adk", password="pass")
    service = ADKChatService()

    def fake_run(**kwargs):
        yield DummyEvent("ok")

    monkeypatch.setattr(service.runner, "run", fake_run)

    msg = service.send_message(user, "hello")

    assert msg.sender == Message.AGENT
    assert msg.content_type == Message.TEXT
    conv = service.get_conversation(user)
    assert conv.messages.count() == 2
