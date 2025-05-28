from .base import BaseAgent
from app.models import Message


class CashFlowAgent(BaseAgent):
    name = "cash_flow"

    def handle_message(self, text: str):
        return Message.TEXT, {"text": "Here is your cash flow summary."}
