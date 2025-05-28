from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase

from app.models import Conversation, Message

class ChatAPITest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test", password="pass")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_send_message_creates_reply(self):
        res = self.client.post("/api/chat/send/", {"text": "hello"}, format="json")
        self.assertEqual(res.status_code, 200)
        conv = Conversation.objects.get(user=self.user)
        self.assertEqual(conv.messages.count(), 2)

    def test_history_returns_messages(self):
        conv = Conversation.objects.create(user=self.user)
        Message.objects.create(conversation=conv, sender="user", content_type="text", payload={"text": "hi"})
        res = self.client.get("/api/chat/history/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
