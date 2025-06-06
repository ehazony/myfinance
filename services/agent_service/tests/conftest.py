"""Test fixtures for the agent service test suite.

Provides a lightweight stub of the ``google.adk`` package so the
agent modules can be imported without installing external
dependencies.
"""

import types
import sys
import importlib
import pytest

# Create stubs for external dependencies before test modules import them
if 'google' not in sys.modules:
    sys.modules['google'] = types.ModuleType('google')
google = sys.modules['google']
adk = types.ModuleType('google.adk')
agents = types.ModuleType('google.adk.agents')
tools_mod = types.ModuleType('google.adk.tools')
def google_search(query):
    return f"search:{query}"
tools_mod.google_search = google_search
tool_context_mod = types.ModuleType('google.adk.tools.tool_context')
class ToolContext:
    def __init__(self):
        self.state = {}
tool_context_mod.ToolContext = ToolContext
sessions_mod = types.ModuleType('google.adk.sessions')
class Session: pass
class InMemorySessionService: pass
sessions_mod.Session = Session
sessions_mod.InMemorySessionService = InMemorySessionService
memory_mod = types.ModuleType('google.adk.memory')
class InMemoryMemoryService: pass
memory_mod.InMemoryMemoryService = InMemoryMemoryService

class DummyAgent:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

agents.Agent = DummyAgent
adk.agents = agents
adk.tools = tools_mod
adk.sessions = sessions_mod
adk.memory = memory_mod
google.adk = adk
sys.modules['google.adk'] = adk
sys.modules['google.adk.agents'] = agents
sys.modules['google.adk.tools'] = tools_mod
sys.modules['google.adk.tools.tool_context'] = tool_context_mod
sys.modules['google.adk.sessions'] = sessions_mod
sys.modules['google.adk.memory'] = memory_mod

# Ensure the service package can be imported as ``agents_adk``
# Stub heavy OpenAPI client modules used by FinanceDataClient
if '_client' not in sys.modules:
    sys.modules['_client'] = types.ModuleType('_client')
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

# Import the real service package as ``agents_adk`` now that heavy deps are stubbed
sys.modules.setdefault(
    'agents_adk', importlib.import_module('services.agent_service.agents_adk')
)

# Stub finance_data_client used by finance tools
fdc = types.ModuleType('tools.finance_data_client')
def get_finance_client():
    class Dummy:
        pass
    return Dummy()
fdc.get_finance_client = get_finance_client
sys.modules['tools.finance_data_client'] = fdc

@pytest.fixture(autouse=True)
def stub_google_adk():
    """Autouse fixture to ensure stubs remain active."""
    yield
