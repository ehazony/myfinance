from .base import BaseAgent
from app.models import Message


class DebtStrategyAgent(BaseAgent):
    name = "debt_strategy"
    schema_file = "DebtStrategy.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload 