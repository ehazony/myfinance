from .base import BaseAgent
from app.models import Message


class TaxPensionAgent(BaseAgent):
    name = "tax_pension"

    def handle_message(self, text: str):
        return Message.TEXT, {"text": "Here is your tax and pension info."}
