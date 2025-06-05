def mock_completion(model=None, messages=None, mock_response="{}"):
    return {"mock_response": mock_response}

def completion(model=None, messages=None, **kwargs):
    return mock_completion(model, messages, mock_response=kwargs.get("mock_response", "{}"))
