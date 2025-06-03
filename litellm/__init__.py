"""Minimal stub of the litellm package for offline testing."""

def mock_completion(*, model=None, messages=None, mock_response="{\"ok\": true}"):
    return {"choices": [{"message": {"content": mock_response}}]}

def completion(model, messages, **kwargs):
    return mock_completion(model=model, messages=messages, mock_response=kwargs.get("mock_response", "{""ok"": true}"))
