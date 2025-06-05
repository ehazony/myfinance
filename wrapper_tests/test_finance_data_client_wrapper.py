import asyncio
from typing import Union
import types
import sys
import os

import pytest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide lightweight stubs for the generated client modules
client_stub = types.ModuleType("_client.client")
client_stub.AuthenticatedClient = object
client_stub.Client = object
sys.modules["_client.client"] = client_stub

api_stub = types.ModuleType("_client.api.api")
async def dummy_asyncio_detailed(**kwargs):
    return kwargs
api_stub.api_agent_financial_context_retrieve = types.SimpleNamespace(asyncio_detailed=dummy_asyncio_detailed)
api_stub.api_agent_transactions_list = types.SimpleNamespace(asyncio_detailed=dummy_asyncio_detailed)
api_stub.api_agent_budget_analysis_list = types.SimpleNamespace(asyncio_detailed=dummy_asyncio_detailed)
api_stub.api_agent_account_summary_list = types.SimpleNamespace(asyncio_detailed=dummy_asyncio_detailed)
api_stub.api_agent_conversation_context_retrieve = types.SimpleNamespace(asyncio_detailed=dummy_asyncio_detailed)
sys.modules["_client.api.api"] = api_stub

types_stub = types.ModuleType("_client.types")
class Unset: pass
UNSET = Unset()
types_stub.UNSET = UNSET
types_stub.Unset = Unset
types_stub.Response = dict
sys.modules["_client.types"] = types_stub

errors_stub = types.ModuleType("_client.errors")
errors_stub.UnexpectedStatus = Exception
sys.modules["_client.errors"] = errors_stub

models_stub = types.ModuleType("_client.models")
models_stub.FinancialContext = object
models_stub.Transaction = object
models_stub.BudgetTarget = object
models_stub.AccountSummary = object
models_stub.ConversationContext = object
sys.modules["_client.models"] = models_stub

from services.agent_service.tools.finance_data_client import FinanceDataClient, SyncFinanceDataClient

# Dummy async function to emulate generated client call
async def _dummy_api(*, client, val: Union[Unset, int] = UNSET, maybe_none: Union[Unset, None, int] = UNSET):
    return {
        "val": val,
        "maybe_none": maybe_none,
    }

def test_sanitize_kwargs_none_converted():
    client = FinanceDataClient()
    kwargs = {"client": object(), "val": None, "maybe_none": None}
    sanitized = client._sanitize_kwargs(_dummy_api, kwargs)
    assert sanitized["val"] is UNSET
    assert sanitized["maybe_none"] is None

def test_run_async_with_running_loop():
    sync_client = SyncFinanceDataClient()

    async def sample():
        return "ok"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = sync_client._run_async(sample())
        assert result == "ok"
    finally:
        loop.close()
        asyncio.set_event_loop(None)
