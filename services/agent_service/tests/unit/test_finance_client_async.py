"""Unit tests for SyncFinanceDataClient asynchronous execution helpers."""

import asyncio
import sys
import types

# Stub out heavy _client modules before importing the finance client
sys.modules.setdefault('_client', types.ModuleType('_client'))
client_mod = types.ModuleType('_client.client')
client_mod.Client = object
client_mod.AuthenticatedClient = object
sys.modules.setdefault('_client.client', client_mod)
api_mod = types.ModuleType('_client.api.api')
api_mod.api_agent_financial_context_retrieve = object
api_mod.api_agent_transactions_list = object
api_mod.api_agent_budget_analysis_list = object
api_mod.api_agent_account_summary_list = object
api_mod.api_agent_conversation_context_retrieve = object
sys.modules.setdefault('_client.api.api', api_mod)
models_mod = types.ModuleType('_client.models')
models_mod.FinancialContext = object
models_mod.Transaction = object
models_mod.BudgetTarget = object
models_mod.AccountSummary = object
models_mod.ConversationContext = object
sys.modules.setdefault('_client.models', models_mod)
types_mod = types.ModuleType('_client.types')
types_mod.Response = object
types_mod.UNSET = object
sys.modules.setdefault('_client.types', types_mod)
errors_mod = types.ModuleType('_client.errors')
errors_mod.UnexpectedStatus = Exception
sys.modules.setdefault('_client.errors', errors_mod)

from services.agent_service.tools.finance_data_client import SyncFinanceDataClient


class DummyClient(SyncFinanceDataClient):
    async def get_financial_context(self, token: str, **kwargs):
        await asyncio.sleep(0)
        return {"token": token, **kwargs}


def test_run_async_inside_event_loop():
    """_run_async should work when an event loop is already running."""

    client = DummyClient()

    async def run():
        return client.get_financial_context_sync("tok", limit_transactions=1)

    result = asyncio.run(run())
    assert result == {"token": "tok", "limit_transactions": 1}
