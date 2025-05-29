from .base import BaseAgent
from app.models import Message


class ReportingAgent(BaseAgent):
    name = "reporting"
    schema_file = "Report.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.CHART, payload
