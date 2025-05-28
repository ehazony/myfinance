from typing import Tuple, Dict

from app.models import Message


class BaseAgent:
    """Simple base class for all agents."""

    name: str = "agent"

    def handle_message(self, text: str) -> Tuple[str, Dict]:
        """Process the message and return content type and payload."""
        raise NotImplementedError
