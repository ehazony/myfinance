import datetime

import pytest
from django.contrib.auth import get_user_model

from app.services.chat_service import ChatService
from app.models import Message
from myFinance.models import (
    Tag,
    TransactionNameTag,
    TagGoal,
    Transaction,
    DateInput,
)


@pytest.mark.django_db
def test_send_message_creates_reply(orchestrator_llm):
    user = get_user_model().objects.create_user(username="tester", password="pass")
    service = ChatService()
    msg = service.send_message(user, "show me a chart")

    assert msg.sender == Message.AGENT
    assert msg.content_type == Message.TEXT

    conv = service.get_conversation(user)
    assert conv.messages.count() == 2


@pytest.mark.django_db
def test_build_financial_context(monkeypatch):
    user = get_user_model().objects.create_user(username="ctx", password="pass")

    DateInput.objects.create(user=user, name="start_date", date=datetime.date.today())

    tag = Tag.objects.create(user=user, name="Food", key="food")
    TransactionNameTag.objects.create(user=user, transaction_name="Shop", tag=tag)
    TagGoal.objects.create(user=user, tag=tag, value=250)
    Transaction.objects.create(user=user, name="Shop", value=10, date=datetime.date.today(), tag=tag)

    service = ChatService()
    txns, category_map, budgets = service.build_financial_context(user)

    assert len(txns) == 1
    assert category_map == {"Shop": "Food"}
    assert budgets == {"Food": 250}


@pytest.mark.django_db
def test_send_message_passes_context(monkeypatch):
    user = get_user_model().objects.create_user(username="patch", password="pass")

    Tag.objects.create(user=user, name="Other", key="other")

    service = ChatService()

    captured = {}

    def fake_handle_message(text, **kwargs):
        captured.update(kwargs)
        return Message.TEXT, {"text": "ok"}

    monkeypatch.setattr(service.orchestrator, "handle_message", fake_handle_message)

    service.send_message(user, "cash flow please")

    assert "transactions" in captured
    assert "category_map" in captured
    assert "budget_targets" in captured

