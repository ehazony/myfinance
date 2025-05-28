from .base import BaseAgent
from app.models import Message


class TaxPensionAgent(BaseAgent):
    name = "tax_pension"
    schema_file = "TaxPensionProfile.json"

    def handle_message(self, text: str):
        payload = {
            "profile_id": "00000000-0000-0000-0000-000000000000",
            "tax_year": 2024,
            "gross_income": 0,
            "pension_plans": []
        }
        self.validate_payload(payload)
        return Message.TEXT, payload
