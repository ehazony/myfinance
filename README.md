# Finance Project

## Testing Guide

For comprehensive instructions on testing the ADK Finance Agent system, see:
- [ADK Finance Agent Testing Guide](agents_adk/README_TESTING.md)

This guide covers all available testing scripts, scenarios, troubleshooting, and best practices.

Unit tests for the agent service live under `services/agent_service/tests/unit`,
component tests under `services/agent_service/tests/component`, and end-to-end tests under
`services/agent_service/tests/e2e`.

## API Key Setup & Cost Efficiency Warning

To use Gemini-powered features, you must set the `GEMINI_API_KEY` in your `.env` file:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

⚠️ **Cost Efficiency Notice:**  
Before running any tests that use the Gemini API, always consider cost efficiency. Only use the API and run relevant tests if you have made changes that require Gemini-powered features. Avoid unnecessary or broad test runs to prevent excessive API usage and costs.

## Documentation Reference

For detailed technical documentation and API references, see:
- [Google ADK Python Complete Reference](docs/references/google-adk-python-complete-reference.md)

This document provides in-depth information about the system's integration with Google ADK and related APIs.
A shared `finance_common` package now provides SQLAlchemy implementations of the main Django models so services can access the database without duplicating code.
