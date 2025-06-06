"""Component tests for the ADKChatService send_message flow."""

import importlib
import sys
import asyncio

# Ensure ``agents_adk`` import resolves to the local service package
sys.modules.setdefault(
    "agents_adk", importlib.import_module("services.agent_service.agents_adk")
)

from services.agent_service.services.adk_chat_service import ADKChatService


class DummyChatService(ADKChatService):
    async def process_message(self, user_id: str, text: str, context=None):
        return {"content": f"processed {text}", "metadata": {}}


def test_send_message_returns_processed_text():
    service = DummyChatService()
    content_type, payload = asyncio.run(service.send_message("u1", "hello"))
    assert content_type == "text"
    assert payload["message"] == "processed hello"
