from .base import BaseAgent
from app.models import Message


class SafetyAgent(BaseAgent):
    name = "safety"

    def handle_message(self, text: str):
        return Message.TEXT, {"text": "Safety checks complete."}
