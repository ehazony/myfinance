from .base import BaseAgent
from app.models import Message


class OnboardingAgent(BaseAgent):
    name = "onboarding"
    schema_file = "BaselineSnapshot.json"

    def handle_message(self, text: str):
        lower = text.lower()
        if "button" in lower:
            return Message.BUTTONS, {"buttons": ["Yes", "No"]}
        if "image" in lower:
            return Message.IMAGE, {"url": "https://placekitten.com/300/200"}
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload
