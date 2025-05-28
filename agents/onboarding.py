from .base import BaseAgent
from app.models import Message


class OnboardingAgent(BaseAgent):
    name = "onboarding"

    def handle_message(self, text: str):
        lower = text.lower()
        if "button" in lower:
            return Message.BUTTONS, {"buttons": ["Yes", "No"]}
        if "image" in lower:
            return Message.IMAGE, {"url": "https://placekitten.com/300/200"}
        return Message.TEXT, {"text": f"Welcome! {text}"}
