# Agent Setup Recommendations

This file is for documenting any setup issues encountered during installation or configuration of the project. If you encounter a problem, please describe exactly what is missing and how you recommend it be fixed.

## Missing `litellm` Package

Running the test suite fails with `ModuleNotFoundError: No module named 'litellm'`.
The `requirements/agents.txt` file lists `litellm`, but the package isn't installed in the test environment. Attempting to `pip install` the package fails because network access is disabled.

**Recommendation:** add `litellm` to the default environment or vendor a local wheel so the tests can run without internet access.

## Missing `plotly` Package

The Django settings import the reporting agent which depends on `plotly`. Tests fail with `ModuleNotFoundError: No module named 'plotly'` when importing `agents.reporting`. Ensure `plotly` is installed or provide a lightweight stub for the test environment.

## Missing `langgraph` Package

Workflow code imports `langgraph.graph` for building conversation graphs. Without the package, tests raise `ModuleNotFoundError: No module named 'langgraph'`. Install `langgraph` or include a minimal stub so workflows can be loaded during testing.
