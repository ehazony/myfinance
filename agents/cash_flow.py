from .base import BaseAgent
from app.models import Message


class CashFlowAgent(BaseAgent):
    name = "cash_flow"
    schema_file = "CashFlowLedger.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload
