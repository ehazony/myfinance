from .base import BaseAgent
from app.models import Message


class InvestmentAgent(BaseAgent):
    name = "investment"

    def handle_message(self, text: str):
        return Message.TEXT, {"text": "Final investment advice."}
