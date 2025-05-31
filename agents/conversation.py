from .base import BaseAgent
from app.models import Message

class ConversationAgent(BaseAgent):
    """Summarise Data-lane outputs into user-facing text."""

    name = "conversation"
    schema_file = None

    def handle_message(self, text: str, *, source: str, agent: str, payload: dict) -> tuple[str, dict]:
        summary = f"{agent} completed"
        missing = payload.get("missing_info") if isinstance(payload, dict) else None
        if missing:
            summary += ": missing " + ", ".join(missing)
        return Message.TEXT, {"messages": [summary]}

