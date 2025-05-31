"""
Integration Tests Package

This package contains integration tests that make real API calls
and test the complete system behavior without mocking.

These tests are separate from unit tests and require:
- Real API keys (OPENAI_API_KEY, etc.)
- Network connectivity
- May incur costs

Run with: pytest integration_tests/
""" 