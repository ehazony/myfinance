"""
Integration Tests for Orchestrator with Real LLM Calls

These tests make actual API calls to LLM providers and test the complete
orchestrator flow without any mocking. They require:

1. Valid API keys (OPENAI_API_KEY or ANTHROPIC_API_KEY)
2. Network connectivity
3. Will incur API costs

To run:
    pytest integration_tests/test_orchestrator_real_llm.py -v -s

To skip if no API key is configured, the tests will automatically skip
with an appropriate message.
"""

import os
import pytest
import logging
from agents.orchestrator import Orchestrator
from app.models import Message

# Enable debug logging to see LLM interactions
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestOrchestratorRealLLM:
    """Integration tests that make real LLM API calls."""

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY to run integration tests."
    )
    def test_orchestrator_hi_greeting_real_response(self):
        """
        Test orchestrator response to 'hi' with real LLM calls.
        
        This verifies:
        1. LLM routing works or falls back to heuristics appropriately
        2. Conversation agent generates a real greeting response
        3. Response structure is correct
        4. Response content indicates real LLM interaction (not fallback)
        """
        logger.info("Testing orchestrator with real LLM for 'hi' greeting")
        
        # Arrange
        orchestrator = Orchestrator()
        user_message = "hi"
        
        # Act
        content_type, payload = orchestrator.handle_message(user_message)
        
        # Assert basic structure
        assert content_type == Message.TEXT, f"Expected TEXT content type, got {content_type}"
        assert isinstance(payload, dict), f"Expected dict payload, got {type(payload)}"
        assert "messages" in payload, f"Expected 'messages' key in payload, got keys: {payload.keys()}"
        assert isinstance(payload["messages"], list), f"Expected messages to be a list"
        assert len(payload["messages"]) > 0, "Expected at least one message in response"
        
        # Get the response message
        response_message = payload["messages"][0]
        assert isinstance(response_message, str), f"Expected string message, got {type(response_message)}"
        assert len(response_message) > 0, "Expected non-empty response"
        
        # Log the response for analysis
        print(f"\n=== ORCHESTRATOR REAL LLM TEST RESULTS ===")
        print(f"User Input: {user_message}")
        print(f"Content Type: {content_type}")
        print(f"Response Message: {response_message}")
        print(f"Full Payload: {payload}")
        print(f"Response Length: {len(response_message)} characters")
        
        # Verify this is NOT a generic fallback response
        fallback_responses = ["Task completed", "ok", "true"]
        is_fallback = any(response_message.lower().strip() == fallback.lower() 
                         for fallback in fallback_responses)
        
        assert not is_fallback, f"Got fallback response: '{response_message}'. This suggests LLM calls are not working."
        
        # For a greeting, expect a substantial response with relevant content
        assert len(response_message) > 10, f"Response too short ({len(response_message)} chars): '{response_message}'"
        
        # Check for greeting-like content
        greeting_indicators = [
            'hello', 'hi', 'help', 'assist', 'finance', 'financial', 
            'welcome', 'how can i', 'what can i', 'good', 'great'
        ]
        message_lower = response_message.lower()
        has_greeting_content = any(indicator in message_lower for indicator in greeting_indicators)
        
        if has_greeting_content:
            print(f"✅ SUCCESS: Response contains greeting-like content")
        else:
            print(f"⚠️  WARNING: Response doesn't contain typical greeting indicators")
            print(f"   This might still be valid if the LLM chose an unconventional response")

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured."
    )
    def test_orchestrator_routing_with_real_llm(self):
        """
        Test that orchestrator routing works with real LLM calls.
        
        This tests just the routing decision for 'hi' message.
        """
        logger.info("Testing orchestrator routing with real LLM")
        
        # Arrange
        orchestrator = Orchestrator()
        user_message = "how are you doing?"
        
        # Act
        selected_agent = orchestrator.route(user_message)
        
        # Assert
        expected_agents = ["conversation", "onboarding"]
        assert selected_agent in expected_agents, (
            f"Expected 'hi' to route to one of {expected_agents}, got '{selected_agent}'"
        )
        
        print(f"\n=== ROUTING TEST RESULTS ===")
        print(f"User Input: {user_message}")
        print(f"Selected Agent: {selected_agent}")
        print(f"✅ Routing working correctly")

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"),
        reason="No LLM API key configured."
    )
    def test_orchestrator_casual_greeting_response(self):
        """
        Test orchestrator response to casual greeting 'how are you going' with real LLM calls.
        
        This tests a more casual greeting pattern to see how the system handles it.
        """
        logger.info("Testing orchestrator with casual greeting 'how are you going'")
        
        # Arrange
        orchestrator = Orchestrator()
        user_message = "how are you going"
        
        # Act
        content_type, payload = orchestrator.handle_message(user_message)
        
        # Assert basic structure
        assert content_type == Message.TEXT, f"Expected TEXT content type, got {content_type}"
        assert isinstance(payload, dict), f"Expected dict payload, got {type(payload)}"
        assert "messages" in payload, f"Expected 'messages' key in payload, got keys: {payload.keys()}"
        assert isinstance(payload["messages"], list), f"Expected messages to be a list"
        assert len(payload["messages"]) > 0, "Expected at least one message in response"
        
        # Get the response message
        response_message = payload["messages"][0]
        assert isinstance(response_message, str), f"Expected string message, got {type(response_message)}"
        assert len(response_message) > 0, "Expected non-empty response"
        
        # Log the response for analysis
        print(f"\n=== ORCHESTRATOR CASUAL GREETING TEST RESULTS ===")
        print(f"User Input: {user_message}")
        print(f"Content Type: {content_type}")
        print(f"Response Message: {response_message}")
        print(f"Full Payload: {payload}")
        print(f"Response Length: {len(response_message)} characters")
        
        # For casual greetings, we should get SOME response, not a fallback
        # The system might route it differently but should handle it gracefully
        fallback_responses = ["Task completed", "ok", "true"]
        is_fallback = any(response_message.lower().strip() == fallback.lower() 
                         for fallback in fallback_responses)
        
        if is_fallback:
            print(f"⚠️  Got fallback response - this suggests the system couldn't handle this greeting pattern")
        else:
            print(f"✅ Got substantive response - system handled casual greeting")
        
        # Verify minimum response quality
        assert len(response_message) > 5, f"Response too short ({len(response_message)} chars): '{response_message}'" 