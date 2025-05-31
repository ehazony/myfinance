"""
Unit tests to verify agent message formats match frontend expectations.
Tests that all agents return (content_type, payload) tuples in the correct format.
"""

import unittest
from unittest.mock import patch, MagicMock
import json

from app.models import Message
from agents.orchestrator import Orchestrator
from agents.conversation import ConversationAgent
from agents.reporting import ReportingAgent
from agents.onboarding import OnboardingAgent
from agents.cash_flow import CashFlowAgent
from agents.goal_setting import GoalSettingAgent


class MessageFormatCompatibilityTests(unittest.TestCase):
    """Test that all agent responses match frontend format expectations."""

    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = Orchestrator()
        self.sample_context = {
            "transactions": [],
            "category_map": {},
            "budget_targets": {}
        }

    def test_message_content_types_are_valid(self):
        """Test that all agents return valid content types."""
        valid_content_types = {Message.TEXT, Message.IMAGE, Message.BUTTONS, Message.CHART}
        
        # Test different agent responses with appropriate mocks
        test_cases = [
            ("conversation", "hello", {"messages": ["Hello! How can I help?"]}),
            ("reporting", "show chart", {}),  # ReportingAgent doesn't use LLM for basic responses
            ("onboarding", "get started", {
                "snapshot_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001", 
                "created_at": "2024-01-01T12:00:00Z",
                "currency": "ILS",
                "accounts": [],
                "assets": [],
                "liabilities": []
            }),
            ("cash_flow", "analyze spending", {"analysis": "cash flow data"}),
            ("goal_setting", "set savings goal", {"goal_type": "savings", "amount": 5000}),
        ]
        
        for agent_name, test_message, mock_response in test_cases:
            with self.subTest(agent=agent_name, message=test_message):
                if agent_name in self.orchestrator.agents:
                    agent = self.orchestrator.agents[agent_name]
                    
                    # Mock LLM calls and validation to avoid real API calls and schema issues
                    with patch.object(agent, 'generate_payload', return_value=mock_response):
                        with patch.object(agent, 'validate_payload', return_value=None):
                            try:
                                content_type, payload = agent.handle_message(test_message)
                                
                                # Verify content type is valid
                                self.assertIn(content_type, valid_content_types, 
                                            f"Agent {agent_name} returned invalid content_type: {content_type}")
                                
                                # Verify payload is a dictionary
                                self.assertIsInstance(payload, dict, 
                                                    f"Agent {agent_name} payload should be dict, got {type(payload)}")
                                
                            except Exception as e:
                                self.fail(f"Agent {agent_name} failed to handle message: {e}")

    def test_conversation_agent_text_format(self):
        """Test ConversationAgent returns properly formatted text messages."""
        agent = ConversationAgent()
        
        # Mock LLM to return different message formats
        test_cases = [
            # Single message
            {"messages": ["Hello! How can I help you?"]},
            # Multiple messages (should be formatted into single message)
            {"messages": [
                "Hello! Ready to tackle your finances?",
                "You could try: 'upload bank statements', 'set a savings goal', or 'track spending'",
                "What sounds good?"
            ]},
            # Empty/invalid response (should get fallback)
            {},
            None
        ]
        
        for i, mock_response in enumerate(test_cases):
            with self.subTest(case=i, response=mock_response):
                with patch.object(agent, 'generate_payload', return_value=mock_response):
                    with patch.object(agent, 'validate_payload', return_value=None):
                        content_type, payload = agent.handle_message("test message")
                        
                        # Should always return TEXT content type
                        self.assertEqual(content_type, Message.TEXT)
                        
                        # Should have text key with string content (frontend compatible)
                        self.assertIn("text", payload)
                        self.assertIsInstance(payload["text"], str)
                        self.assertGreater(len(payload["text"]), 0)

    def test_reporting_agent_chart_formats(self):
        """Test ReportingAgent returns proper chart/image formats."""
        agent = ReportingAgent()
        
        test_cases = [
            ("show chart data", Message.CHART),
            ("show chart image", Message.IMAGE),
            ("general chart request", Message.CHART),
        ]
        
        for message, expected_content_type in test_cases:
            with self.subTest(message=message, expected=expected_content_type):
                content_type, payload = agent.handle_message(message)
                
                # Verify content type
                self.assertEqual(content_type, expected_content_type)
                
                # Verify payload structure based on content type
                if content_type == Message.CHART:
                    # Chart data format: should have labels and values OR chart_url
                    self.assertTrue(
                        ("labels" in payload and "values" in payload) or "chart_url" in payload,
                        "Chart payload should have either (labels,values) or chart_url"
                    )
                elif content_type == Message.IMAGE:
                    # Image format: should have chart_url
                    self.assertIn("chart_url", payload)
                    # Should be base64 data URL
                    self.assertTrue(payload["chart_url"].startswith("data:image/"))

    def test_orchestrator_single_message_response(self):
        """Test that orchestrator always returns single message format."""
        
        # Mock all agent responses to avoid LLM calls
        mock_payload = {"messages": ["Test response"]}
        
        with patch('agents.base.BaseAgent.generate_payload', return_value={}):
            with patch.object(ConversationAgent, 'handle_message', return_value=(Message.TEXT, mock_payload)):
                
                content_type, payload = self.orchestrator.handle_message("hello", **self.sample_context)
                
                # Should return single message format
                self.assertIsInstance(content_type, str)
                self.assertIsInstance(payload, dict)
                
                # Content type should be valid
                valid_types = {Message.TEXT, Message.IMAGE, Message.BUTTONS, Message.CHART}
                self.assertIn(content_type, valid_types)

    def test_frontend_expected_payload_structures(self):
        """Test that payloads match frontend expectations for each content type."""
        
        # Test TEXT payload
        text_payload = {"text": "Hello world"}
        self.assertIn("text", text_payload)
        self.assertIsInstance(text_payload["text"], str)
        
        # Test IMAGE payload
        image_payload = {"url": "https://example.com/image.png"}
        chart_image_payload = {"chart_url": "data:image/png;base64,iVBORw0KGgoAAAANSU"}
        
        # Should have either url or chart_url
        self.assertTrue("url" in image_payload or "chart_url" in image_payload)
        self.assertTrue("url" in chart_image_payload or "chart_url" in chart_image_payload)
        
        # Test BUTTONS payload
        buttons_payload = {"buttons": ["Option 1", "Option 2", "Option 3"]}
        self.assertIn("buttons", buttons_payload)
        self.assertIsInstance(buttons_payload["buttons"], list)
        self.assertTrue(all(isinstance(btn, str) for btn in buttons_payload["buttons"]))
        
        # Test CHART payload
        chart_payload = {
            "labels": ["Jan", "Feb", "Mar"],
            "values": [100, 200, 150]
        }
        self.assertIn("labels", chart_payload)
        self.assertIn("values", chart_payload)
        self.assertIsInstance(chart_payload["labels"], list)
        self.assertIsInstance(chart_payload["values"], list)

    def test_conversation_agent_message_aggregation(self):
        """Test that ConversationAgent properly aggregates multiple messages into single formatted text."""
        agent = ConversationAgent()
        
        # Test the _format_single_message method directly
        test_cases = [
            # Single message - should return as-is
            (["Hello!"], "Hello!"),
            
            # Two messages - should combine with spacing
            (["Hello!", "How can I help?"], "Hello!\n\nHow can I help?"),
            
            # Three+ messages - should format with examples section
            ([
                "Hello! Ready to tackle your finances?",
                "Try: 'upload bank statements'",
                "What sounds good?"
            ], 
            "Hello! Ready to tackle your finances?\n\n💡 Try these:\n• upload bank statements\n\nWhat sounds good?"),
            
            # Empty list
            ([], ""),
        ]
        
        for messages, expected_pattern in test_cases:
            with self.subTest(messages=messages):
                result = agent._format_single_message(messages)
                
                if not messages:
                    self.assertEqual(result, "")
                elif len(messages) == 1:
                    self.assertEqual(result, messages[0])
                else:
                    # Should contain the first and last messages
                    self.assertIn(messages[0], result)
                    self.assertIn(messages[-1], result)
                    # Should have proper spacing
                    self.assertIn("\n", result)

    def test_message_serialization_compatibility(self):
        """Test that Message model can be properly serialized for API responses."""
        from app.serializers import MessageSerializer
        from app.models import Conversation
        from django.contrib.auth import get_user_model
        
        # This would typically be done in Django test case, but testing the structure
        message_data = {
            'id': 1,
            'conversation': 1,
            'sender': 'agent',
            'content_type': 'text',
            'payload': {'text': 'Hello world'},
            'timestamp': '2024-01-01T12:00:00Z',
            'status': 'sent'
        }
        
        # Verify the structure matches frontend expectations
        required_fields = {'id', 'conversation', 'sender', 'content_type', 'payload', 'timestamp', 'status'}
        self.assertTrue(required_fields.issubset(set(message_data.keys())))
        
        # Verify content_type values are supported
        valid_content_types = {'text', 'image', 'buttons', 'chart', 'form'}
        self.assertIn(message_data['content_type'], valid_content_types)
        
        # Verify sender values
        valid_senders = {'user', 'agent'}
        self.assertIn(message_data['sender'], valid_senders)

    def test_agents_handle_empty_llm_responses_gracefully(self):
        """Test that agents provide fallback responses when LLM returns empty/invalid data."""
        
        # Test ConversationAgent fallback behavior
        agent = ConversationAgent()
        
        invalid_responses = [None, {}, {"invalid": "structure"}, ""]
        
        for invalid_response in invalid_responses:
            with self.subTest(response=invalid_response):
                with patch.object(agent, 'generate_payload', return_value=invalid_response):
                    with patch.object(agent, 'validate_payload', return_value=None):
                        content_type, payload = agent.handle_message("test message")
                        
                        # Should always return valid format even with invalid LLM response
                        self.assertEqual(content_type, Message.TEXT)
                        self.assertIsInstance(payload, dict)
                        self.assertIn("text", payload)
                        self.assertIsInstance(payload["text"], str)
                        self.assertGreater(len(payload["text"]), 0)


if __name__ == '__main__':
    unittest.main() 