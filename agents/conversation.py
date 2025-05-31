import json
from typing import Any

from .base import BaseAgent
from .manifest import load_manifest
from app.models import Message

class ConversationAgent(BaseAgent):
    """Summarise data agent outputs or user queries into short replies."""

    name = "conversation"
    schema_file = "ConversationMessages.json"

    def __init__(self, manifest_path: str | None = None) -> None:
        self.manifest = load_manifest(manifest_path)

    def system_prompt(self) -> str:
        base = super().system_prompt()
        caps = [
            {"name": a["name"], "user_friendly": a.get("user_friendly", "")}
            for a in self.manifest.get("agents", [])
        ]
        manifest_obj = json.dumps({"capabilities": caps}, ensure_ascii=False)
        return base + "\n" + manifest_obj

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

