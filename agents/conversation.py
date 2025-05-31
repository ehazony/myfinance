import json

from .base import BaseAgent
from app.models import Message

class ConversationAgent(BaseAgent):
    """Summarise data agent outputs or user queries into short replies."""

    name = "conversation"
    schema_file = "ConversationMessages.json"

    def handle_message(
        self,
        text: str,
        *,
        source: str,
        agent: str | None = None,
        payload: dict | None = None,
    ) -> tuple[str, dict]:
        """Return chat bubbles using an LLM with heuristic fallback."""

        if source == "User":
            input_data = {"source": "User", "text": text}
        else:
            input_data = {"source": "Data", "agent": agent, "payload": payload or {}}

        llm_input = json.dumps(input_data)
        reply = self.generate_payload(llm_input)

        if not isinstance(reply, dict) or "messages" not in reply:
            # Fallback to a simple summary if LLM output is invalid
            summary = f"{agent} completed"
            missing = (
                payload.get("missing_info")
                if isinstance(payload, dict)
                else None
            )
            if missing:
                summary += ": missing " + ", ".join(missing)
            reply = {"messages": [summary]}

        self.validate_payload(reply)
        return Message.TEXT, reply

