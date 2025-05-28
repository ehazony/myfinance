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
        payload = {
            "snapshot_id": "00000000-0000-0000-0000-000000000000",
            "user_id": "00000000-0000-0000-0000-000000000000",
            "created_at": "2024-01-01T00:00:00Z",
            "currency": "USD",
            "accounts": [],
            "assets": [],
            "liabilities": [],
            "monthly_income": 0,
            "monthly_expenses": 0,
            "notes": ""
        }
        self.validate_payload(payload)
        return Message.TEXT, payload
