from .base import BaseAgent
from app.models import Message


class GoalSettingAgent(BaseAgent):
    name = "goal_setting"

    def handle_message(self, text: str):
        return Message.TEXT, {"text": "Let's talk about your financial goals."}
