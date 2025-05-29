from .base import BaseAgent
from app.models import Message


class ReminderSchedulerAgent(BaseAgent):
    name = "reminder_scheduler"
    schema_file = "ReminderTask.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload 