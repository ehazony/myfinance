from dotenv import load_dotenv
load_dotenv()
from typing import Tuple, Dict
import json
import os
import logging
from pathlib import Path
from jsonschema import validate
import litellm
from jsonschema import validate
from app.models import Message

logger = logging.getLogger(__name__)


class BaseAgent:
    """Simple base class for all agents."""

    name: str = "agent"
    schema_file: str | None = None

    def handle_message(self, text: str) -> Tuple[str, Dict]:
        """Process the message and return content type and payload."""
        raise NotImplementedError

    def system_prompt(self) -> str:
        """Return the system prompt for this agent if available."""
        path = Path(__file__).parent / "prompt" / "system_prompt" / f"{self.name}.md"
        return path.read_text() if path.exists() else ""

    def load_schema(self) -> Dict:
        """Load the JSON schema for this agent if defined."""
        if not self.schema_file:
            return {}
        path = Path(__file__).parent / "schema" / self.schema_file
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}

    def validate_payload(self, payload: Dict) -> None:
        """Validate the payload against the agent schema."""
        schema = self.load_schema()
        if schema:
            try:
                validate(instance=payload, schema=schema)
            except Exception as e:
                logger.warning(f"[SCHEMA WARNING] Validation failed: {e}\nPayload: {payload}")
                raise

    def generate_payload(self, text: str) -> Dict:
        """Call the LLM using litellm and return the parsed JSON payload."""
        messages = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": text},
        ]
        model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        try:
            response = litellm.completion(model=model, messages=messages)
            content = response["choices"][0]["message"]["content"]
            logger.debug(f"[LLM DEBUG] Raw LLM output: {content}")
            payload = json.loads(content)
            logger.debug(f"[LLM DEBUG] Parsed payload: {payload}")
        except Exception as e:
            logger.exception("LLM call failed")
            payload = {}
        return payload

