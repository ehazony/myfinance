from .base import BaseAgent
from app.models import Message


class TaxPensionAgent(BaseAgent):
    name = "tax_pension"
    schema_file = "TaxPensionProfile.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload
