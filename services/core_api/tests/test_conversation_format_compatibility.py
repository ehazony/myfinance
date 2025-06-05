"""
Focused tests for ConversationAgent message formatting compatibility with frontend.
Ensures that all conversation responses are properly formatted as single messages.
"""

import unittest
from unittest.mock import patch
import json

from app.models import Message
from agents.conversation import ConversationAgent


class ConversationFormatCompatibilityTests(unittest.TestCase):
    """Test that ConversationAgent produces frontend-compatible message formats."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = ConversationAgent()

    def test_text_payload_format_matches_frontend_expectations(self):
        """Test that conversation responses have the correct text payload structure."""
        
        # Frontend expects: {"text": "message content"}
        # Agent should now return this format correctly
        
        test_cases = [
            {"messages": ["Hello! How can I help you?"]},
            {"messages": ["Welcome!", "Let's get started!", "What would you like to do?"]},
        ]
        
        for mock_response in test_cases:
            with self.subTest(response=mock_response):
                with patch.object(self.agent, 'generate_payload', return_value=mock_response):
                    with patch.object(self.agent, 'validate_payload', return_value=None):
                        content_type, payload = self.agent.handle_message("test")
                        
                        # Should return TEXT content type
                        self.assertEqual(content_type, Message.TEXT)
                        
                        # Should have text structure (frontend compatible)
                        self.assertIn("text", payload)
                        self.assertNotIn("messages", payload)  # Old format should be gone
                        
                        # The text should be a single string (formatted if multiple messages)
                        self.assertIsInstance(payload["text"], str)
                        self.assertGreater(len(payload["text"]), 0)

    def test_message_formatting_preserves_content(self):
        """Test that message formatting doesn't lose important content."""
        
        multi_message_input = [
            "Hello! Ready to tackle your finances?",
            "You could try: 'upload bank statements', 'set a savings goal', or 'track spending'", 
            "What sounds good?"
        ]
        
        result = self.agent._format_single_message(multi_message_input)
        
        # Should contain all key content
        self.assertIn("Hello! Ready to tackle your finances?", result)
        self.assertIn("What sounds good?", result)
        self.assertIn("upload bank statements", result)
        self.assertIn("set a savings goal", result)
        self.assertIn("track spending", result)
        
        # Should have proper structure with examples
        self.assertIn("💡 Try these:", result)
        self.assertIn("•", result)  # Bullet points

    def test_frontend_can_display_formatted_messages(self):
        """Test that formatted messages work with frontend's text rendering."""
        
        # Frontend ChatScreen handles text messages via: {(item.payload as any).text}
        # Our payload structure is now: {"text": "content"} ✓
        
        test_cases = [
            {"messages": ["Simple greeting"]},
            {"messages": [
                "Multi-part message",
                "Try these options", 
                "Pick one to continue"
            ]},
        ]
        
        for mock_response in test_cases:
            with self.subTest(response=mock_response):
                with patch.object(self.agent, 'generate_payload', return_value=mock_response):
                    with patch.object(self.agent, 'validate_payload', return_value=None):
                        content_type, payload = self.agent.handle_message("test")
                        
                        # Verify structure matches what frontend expects to access
                        self.assertEqual(content_type, Message.TEXT)
                        self.assertIn("text", payload)
                        
                        # Frontend can now access: (item.payload as any).text ✓
                        message_content = payload["text"]
                        self.assertIsInstance(message_content, str)
                        self.assertGreater(len(message_content), 0)

    def test_conversation_agent_provides_text_format_for_frontend(self):
        """Test that the conversation agent specifically returns text format expected by frontend."""
        
        # Frontend expects text messages to have {"text": "content"} structure
        
        mock_llm_response = {"messages": ["Hello! I'm here to help with your finances."]}
        
        with patch.object(self.agent, 'generate_payload', return_value=mock_llm_response):
            with patch.object(self.agent, 'validate_payload', return_value=None):
                content_type, payload = self.agent.handle_message("hello")
                
                # Verify the format now matches frontend expectations
                self.assertEqual(content_type, Message.TEXT)
                self.assertIn("text", payload)  # Frontend expects {"text": "content"}
                self.assertNotIn("messages", payload)  # Should not have old format
                
                # Verify the text content is a string
                self.assertIsInstance(payload["text"], str)
                self.assertGreater(len(payload["text"]), 0)
                
                # Document the corrected format
                print(f"Updated ConversationAgent payload format: {payload}")

    def test_fallback_responses_are_frontend_compatible(self):
        """Test that fallback responses when LLM fails are properly formatted."""
        
        # Test various fallback scenarios
        fallback_scenarios = [
            ("User", "greet", None, {}),
            ("User", "help", None, {}),
            ("User", "clarify", None, {"question": "What do you mean?"}),
            ("User", "fallback", None, {}),
            ("Data", None, "reporting", {"chart_data": "sample"}),
        ]
        
        for source, intent, agent, params in fallback_scenarios:
            with self.subTest(source=source, intent=intent, agent=agent):
                with patch.object(self.agent, 'generate_payload', return_value={}):
                    with patch.object(self.agent, 'validate_payload', return_value=None):
                        if source == "User":
                            content_type, payload = self.agent.handle_message(
                                "test", source=source, intent=intent, params=params
                            )
                        else:
                            content_type, payload = self.agent.handle_message(
                                "test", source=source, agent=agent, payload=params
                            )
                        
                        # All fallbacks should return valid text format compatible with frontend
                        self.assertEqual(content_type, Message.TEXT)
                        self.assertIn("text", payload)
                        self.assertNotIn("messages", payload)  # Should use new format
                        self.assertIsInstance(payload["text"], str)
                        self.assertGreater(len(payload["text"]), 0)


if __name__ == '__main__':
    unittest.main() 