from .base import BaseAgent
from app.models import Message


class CashFlowAgent(BaseAgent):
    name = "cash_flow"
    schema_file = "CashFlowLedger.json"

    def handle_message(self, text: str):
        payload = {
            "ledger_id": "00000000-0000-0000-0000-000000000000",
            "snapshot_id": "00000000-0000-0000-0000-000000000000",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31",
            "currency": "USD",
            "transactions": []
        }
        self.validate_payload(payload)
        return Message.TEXT, payload
