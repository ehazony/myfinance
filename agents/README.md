# Finance Agents

This directory contains the LangChain-based agents that power the FinanceAgent application.
Each agent focuses on a specific domain (onboarding, cash-flow, goals, etc.) and
is orchestrated by the `Orchestrator` class.

## Key Files

- `orchestrator.py` – routes user intents to the proper agent.
- `onboarding.py`, `cash_flow.py`, ... – specialist data agents.
- `prompt/system_prompt/` – system prompts for each agent.
- `workflow.py` – example graph-based workflow using `langgraph`.

## Architecture

Design V2 introduces a dedicated **Conversation Agent** that summarizes all data
outputs and guides the user. Data agents now return only strict schemas while
the Conversation Agent returns `{ "messages": [ ... ] }` JSON.
See `docs/agent_design_v2.md` for the full architecture and remaining tasks.

## Running Tests

Execute the project tests from the repository root:

```bash
pytest -q
```

All agent logic is covered by unit tests under `tests/`.
