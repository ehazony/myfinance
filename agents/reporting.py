from .base import BaseAgent
from app.models import Message


class ReportingAgent(BaseAgent):
    name = "reporting"

    def handle_message(self, text: str):
        return Message.CHART, {"labels": ["Jan", "Feb"], "values": [10, 20]}
