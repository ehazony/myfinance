from .base import BaseAgent
from app.models import Message


class InvestmentAgent(BaseAgent):
    name = "investment"
    schema_file = "InvestmentPortfolio.json"

    def handle_message(self, text: str):
        payload = {
            "portfolio_id": "00000000-0000-0000-0000-000000000000",
            "snapshot_date": "2024-01-01",
            "currency": "USD",
            "target_allocation": {},
            "current_allocation": {},
            "holdings": []
        }
        self.validate_payload(payload)
        return Message.TEXT, payload
