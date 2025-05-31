# Integration Tests

This directory contains integration tests that make **real API calls** to external services and test the complete system behavior without mocking.

## ⚠️ Important Notes

- **These tests make real API calls** and will incur costs
- **Requires valid API keys** to run
- **Separate from unit tests** - no shared infrastructure or mocking
- **May fail due to network issues** or rate limiting

## Requirements

### API Keys
Set one or more of these environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Dependencies
The integration tests use the same dependencies as the main project. Ensure you have installed requirements:
```bash
pip install -r requirements.txt
```

## Running Integration Tests

### Run All Integration Tests
```bash
pytest integration_tests/ -v -s
```

### Run Specific Test File
```bash
pytest integration_tests/test_orchestrator_real_llm.py -v -s
```

### Run Specific Test
```bash
pytest integration_tests/test_orchestrator_real_llm.py::TestOrchestratorRealLLM::test_orchestrator_hi_greeting_real_response -v -s
```

### Skip Tests Without API Keys
If no API keys are configured, tests will automatically skip with a message:
```
SKIPPED [1] No LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY to run integration tests.
```

## What These Tests Do

### `test_orchestrator_real_llm.py`
Tests the orchestrator's behavior with real LLM calls:

1. **`test_orchestrator_hi_greeting_real_response`**: Tests that saying "hi" to the orchestrator gets a real, meaningful greeting response from the LLM
2. **`test_orchestrator_routing_with_real_llm`**: Tests that the orchestrator correctly routes messages using real LLM calls

### Expected Output
When tests pass with real LLM calls, you'll see output like:
```
=== ORCHESTRATOR REAL LLM TEST RESULTS ===
User Input: hi
Content Type: text
Response Message: Hello! I'm your personal finance assistant. How can I help you today? 🚀
Response Length: 71 characters
✅ SUCCESS: Response contains greeting-like content
```

## Troubleshooting

### Tests Are Skipping
- Ensure you have set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Check that environment variables are exported in your shell

### Tests Fail with "Got fallback response"
- This indicates the LLM calls are not working properly
- Check your API key is valid and has credits
- Verify network connectivity
- Check for rate limiting

### Tests Fail with Import Errors
- Ensure you're running from the project root directory
- Check that Django settings are properly configured

## Cost Considerations

Each test run makes multiple API calls:
- Orchestrator routing calls
- Conversation agent calls

Estimated cost per full test run: $0.01 - $0.02 USD (depending on LLM model and response length)

## Separation from Unit Tests

These integration tests are completely separate from unit tests (`tests/` directory):
- **No shared fixtures or configuration**
- **Independent Django setup**
- **No mocking interference**
- **Can be run independently**

To run unit tests (fast, with mocking):
```bash
pytest tests/
```

To run integration tests (slower, real API calls):
```bash
pytest integration_tests/
```

## Test Status

✅ **WORKING**: Integration tests successfully make real LLM API calls and test the orchestrator's response to "hi" greetings 