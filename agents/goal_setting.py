from .base import BaseAgent
from app.models import Message


class GoalSettingAgent(BaseAgent):
    name = "goal_setting"
    schema_file = "GoalList.json"

    def handle_message(self, text: str):
        payload = {"goals": []}
        self.validate_payload(payload)
        return Message.TEXT, payload
