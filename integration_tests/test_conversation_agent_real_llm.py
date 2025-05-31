"""
Integration Tests for Conversation Agent with Real LLM Calls

These tests focus specifically on the conversation agent's behavior
when receiving greeting intents and other conversational patterns.

Requirements:
- Valid API keys (OPENAI_API_KEY or ANTHROPIC_API_KEY)
- Network connectivity
- Will incur API costs

To run:
    pytest integration_tests/test_conversation_agent_real_llm.py -v -s
"""

import os
import pytest
import logging
from agents.conversation import ConversationAgent
from app.models import Message

# Enable debug logging to see LLM interactions
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestConversationAgentRealLLM:
    """Integration tests for conversation agent with real LLM calls."""

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY to run integration tests."
    )
    def test_conversation_agent_direct_greeting_hi(self):
        """
        Test conversation agent's direct response to 'hi' with real LLM.
        
        This bypasses the orchestrator and tests the conversation agent directly.
        """
        logger.info("Testing conversation agent direct response to 'hi'")
        
        # Arrange
        agent = ConversationAgent()
        user_message = "hi"
        
        # Act
        content_type, payload = agent.handle_message(user_message)
        
        # Assert
        assert content_type == Message.TEXT, f"Expected TEXT content type, got {content_type}"
        assert isinstance(payload, dict), f"Expected dict payload, got {type(payload)}"
        assert "messages" in payload, f"Expected 'messages' key in payload"
        assert isinstance(payload["messages"], list), f"Expected messages list"
        assert len(payload["messages"]) > 0, "Expected at least one message"
        
        response_message = payload["messages"][0]
        assert isinstance(response_message, str), f"Expected string message"
        assert len(response_message) > 0, "Expected non-empty response"
        
        # Log results
        print(f"\n=== CONVERSATION AGENT DIRECT TEST: 'hi' ===")
        print(f"User Input: {user_message}")
        print(f"Response: {response_message}")
        print(f"Response Length: {len(response_message)} characters")
        print(f"Full Payload: {payload}")
        
        # Verify it's a quality greeting response
        assert len(response_message) > 10, f"Response too short: '{response_message}'"
        
        # Check for greeting-like content
        greeting_indicators = [
            'hello', 'hi', 'help', 'assist', 'finance', 'financial', 
            'welcome', 'how can i', 'what can i', 'good', 'great'
        ]
        message_lower = response_message.lower()
        has_greeting_content = any(indicator in message_lower for indicator in greeting_indicators)
        
        assert has_greeting_content, f"Response doesn't contain greeting-like content: '{response_message}'"
        print("✅ Response contains appropriate greeting content")

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured."
    )
    def test_conversation_agent_various_greetings(self):
        """
        Test conversation agent responses to various greeting patterns.
        """
        logger.info("Testing conversation agent with various greeting patterns")
        
        greetings = [
            "hello",
            "how are you going",
            "good morning",
            "hey there",
            "what's up"
        ]
        
        agent = ConversationAgent()
        results = {}
        
        for greeting in greetings:
            print(f"\n--- Testing greeting: '{greeting}' ---")
            
            # Act
            content_type, payload = agent.handle_message(greeting)
            
            # Basic assertions
            assert content_type == Message.TEXT, f"Expected TEXT for '{greeting}'"
            assert "messages" in payload, f"Expected messages for '{greeting}'"
            assert len(payload["messages"]) > 0, f"Expected response for '{greeting}'"
            
            response = payload["messages"][0]
            results[greeting] = response
            
            print(f"Response: {response}")
            print(f"Length: {len(response)} characters")
            
            # Verify quality
            assert len(response) > 5, f"Response too short for '{greeting}': '{response}'"
            assert response != "Task completed", f"Got fallback for '{greeting}'"
        
        # Print summary
        print(f"\n=== GREETING RESPONSE SUMMARY ===")
        for greeting, response in results.items():
            print(f"'{greeting}' → '{response[:50]}{'...' if len(response) > 50 else ''}'")
        
        # Verify variety (responses shouldn't all be identical)
        unique_responses = set(results.values())
        print(f"\nUnique responses: {len(unique_responses)} out of {len(results)}")
        
        # Allow some similarity but expect some variation
        if len(results) > 2:
            assert len(unique_responses) >= 2, "All responses are identical - lack of natural variation"

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured."
    )
    def test_conversation_agent_help_request(self):
        """
        Test conversation agent's response to help requests.
        """
        logger.info("Testing conversation agent response to help request")
        
        # Arrange
        agent = ConversationAgent()
        user_message = "what can you help me with?"
        
        # Act
        content_type, payload = agent.handle_message(user_message)
        
        # Assert
        assert content_type == Message.TEXT
        assert "messages" in payload
        assert len(payload["messages"]) > 0
        
        response = payload["messages"][0]
        
        print(f"\n=== HELP REQUEST TEST ===")
        print(f"User Input: {user_message}")
        print(f"Response: {response}")
        print(f"Response Length: {len(response)} characters")
        
        # Verify it's a helpful response
        assert len(response) > 20, f"Help response too short: '{response}'"
        
        # Check for help-related content
        help_indicators = [
            'help', 'assist', 'can', 'finance', 'financial', 'budget', 
            'money', 'transaction', 'account', 'goal', 'track'
        ]
        message_lower = response.lower()
        help_content_count = sum(1 for indicator in help_indicators if indicator in message_lower)
        
        assert help_content_count >= 2, f"Response lacks help-related content: '{response}'"
        print("✅ Response contains appropriate help content")

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured."
    )
    def test_conversation_agent_consistency(self):
        """
        Test that conversation agent gives consistent quality responses.
        Run the same greeting multiple times to check for consistency.
        """
        logger.info("Testing conversation agent consistency")
        
        agent = ConversationAgent()
        greeting = "hi"
        responses = []
        
        # Run the same greeting 3 times
        for i in range(3):
            print(f"\n--- Run {i+1}: '{greeting}' ---")
            
            content_type, payload = agent.handle_message(greeting)
            response = payload["messages"][0]
            responses.append(response)
            
            print(f"Response: {response}")
            
            # Each should be a quality response
            assert len(response) > 10, f"Run {i+1} response too short"
            assert response != "Task completed", f"Run {i+1} got fallback response"
        
        print(f"\n=== CONSISTENCY TEST SUMMARY ===")
        for i, response in enumerate(responses, 1):
            print(f"Run {i}: {response}")
        
        # Check that all responses are reasonable length
        avg_length = sum(len(r) for r in responses) / len(responses)
        print(f"Average response length: {avg_length:.1f} characters")
        
        assert avg_length > 15, f"Average response length too short: {avg_length}"
        
        # Responses can be different (that's natural) but should all be greetings
        for i, response in enumerate(responses, 1):
            greeting_indicators = ['hello', 'hi', 'help', 'assist', 'how can']
            has_greeting = any(indicator in response.lower() for indicator in greeting_indicators)
            assert has_greeting, f"Run {i} doesn't seem like a greeting: '{response}'"
        
        print("✅ All responses are consistent greeting-type responses") 