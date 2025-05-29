from .base import BaseAgent
from app.models import Message


class InvestmentAgent(BaseAgent):
    name = "investment"
    schema_file = "InvestmentPortfolio.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload
