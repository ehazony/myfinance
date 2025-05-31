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

    def _format_single_message(self, messages: list[str]) -> str:
        """
        Convert multiple messages into a single, well-structured message for front-end compatibility.
        
        Format:
        - First message as greeting/main content
        - Middle messages as bullet points or examples
        - Last message as call-to-action question
        """
        if not messages:
            return ""
        
        if len(messages) == 1:
            return messages[0]
        
        # Structure the response
        result_parts = []
        
        # Add first message (greeting/main content)
        result_parts.append(messages[0])
        
        # Process middle messages (if any) - format as examples/options
        if len(messages) > 2:
            middle_messages = messages[1:-1]
            
            # Check if any middle message contains examples (has quotes or 'try')
            examples_found = any("'" in msg or '"' in msg or 'try' in msg.lower() for msg in middle_messages)
            
            if examples_found:
                result_parts.append("")  # Add blank line
                result_parts.append("💡 Try these:")
                for msg in middle_messages:
                    # Format as bullet point, clean up the message
                    clean_msg = msg.strip()
                    if clean_msg.startswith("Try:") or clean_msg.startswith("You could try:"):
                        # Extract the part after the colon
                        clean_msg = clean_msg.split(":", 1)[1].strip()
                    result_parts.append(f"• {clean_msg}")
            else:
                # Just add middle messages with spacing
                result_parts.append("")
                result_parts.extend(middle_messages)
        
        # Add blank line before final question
        result_parts.append("")
        
        # Add last message (call-to-action)
        result_parts.append(messages[-1])
        
        return "\n".join(result_parts)

    def handle_message(
        self,
        text: str,
        *,
        source: str = "User",
        agent: str | None = None,
        payload: dict | None = None,
        intent: str | None = None,
        params: dict | None = None,
    ) -> tuple[str, dict]:
        """Return chat bubbles using an LLM with heuristic fallback."""

        if source == "User":
            # Handle direct user requests with intents
            if intent:
                input_data = {"source": "User", "text": text, "intent": intent, "params": params or {}}
            else:
                input_data = {"source": "User", "text": text}
        else:
            input_data = {"source": "Data", "agent": agent, "payload": payload or {}}

        llm_input = json.dumps(input_data)
        reply = self.generate_payload(llm_input)

        if not isinstance(reply, dict) or "messages" not in reply:
            # Always provide a helpful fallback response for users
            if source == "User":
                # Handle specific conversation intents with directive fallbacks
                if intent == "clarify":
                    question = params.get("question", "Could you clarify what you'd like help with?") if params else "Could you clarify what you'd like help with?"
                    reply = {"messages": [question]}
                elif intent == "fallback":
                    reply = {"messages": ["I'm here to help with finances! 💰", "Try: 'track spending', 'set savings goal', or 'upload bank data'", "What interests you?"]}
                elif intent == "greet":
                    reply = {"messages": ["Hello! 😊 Ready to tackle your finances?", "You could try: 'upload bank statements', 'set a savings goal', or 'track spending' 💰", "What sounds good?"]}
                elif intent == "help":
                    reply = {"messages": ["I can help you get organized! Try these: 📊", "'Upload my bank CSV', 'Set goal: save $5000', or 'Show spending by category'", "Pick one to start!"]}
                else:
                    # For any other user input, be conversational but directive
                    reply = {"messages": ["Let's tackle your finances! 🚀", "Try: 'budget this month', 'save for vacation', or 'track expenses'", "Which appeals to you?"]}
            else:
                # Data source fallback
                summary = f"{agent} completed" if agent else "Task completed"
                missing = (
                    payload.get("missing_info")
                    if isinstance(payload, dict)
                    else None
                )
                if missing:
                    summary += ": missing " + ", ".join(missing)
                reply = {"messages": [summary]}

        self.validate_payload(reply)
        
        # Convert multiple messages to single structured message for front-end compatibility
        if "messages" in reply and isinstance(reply["messages"], list):
            if len(reply["messages"]) > 1:
                # Convert to single structured message
                single_message = self._format_single_message(reply["messages"])
                final_text = single_message
            else:
                final_text = reply["messages"][0]
        else:
            final_text = "I'm here to help with your finances!"
        
        # Return frontend-compatible format: {"text": "content"}
        return Message.TEXT, {"text": final_text}

