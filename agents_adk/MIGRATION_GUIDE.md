# Migration Guide: Current Agents → ADK-Based System

This guide explains how to migrate from the current `agents/` system to the new ADK-based system in `agents_adk/`.

## 🎯 Migration Overview

| Current System | ADK System | Status |
|----------------|------------|---------|
| `agents/orchestrator.py` | `agents_adk/agent.py` (root_agent) | ✅ Implemented |
| `agents/onboarding.py` | `agents_adk/agent.py` (onboarding_agent) | ✅ Implemented |
| `agents/cash_flow.py` | `agents_adk/agent.py` (cash_flow_agent) | ✅ Implemented |
| `agents/goal_setting.py` | `agents_adk/agent.py` (goal_setting_agent) | ✅ Implemented |
| `agents/reporting.py` | `agents_adk/agent.py` (reporting_agent) | ✅ Implemented |
| `agents/investment.py` | `agents_adk/agent.py` (investment_agent) | ✅ Implemented |
| `agents/base.py` | Built into ADK framework | ✅ Replaced |
| Django integration | `agents_adk/django_integration.py` | ✅ Implemented |

## 🚀 Getting Started

### 1. Set Up Environment

```bash
# Copy environment template
cp agents_adk/env_template agents_adk/.env

# Edit .env file with your Google API key
# Get one from: https://aistudio.google.com/apikey
```

### 2. Test the System

```bash
cd agents_adk
python test_adk.py
```

### 3. Try Interactive Mode

```bash
# Interactive CLI
adk run agents_adk

# Web UI with development interface
adk web agents_adk
```

## 🔧 Key Improvements

### **Multi-Agent Architecture**
- **Before**: Single orchestrator with manual routing
- **After**: Native ADK multi-agent system with sub_agents
- **Benefit**: Built-in agent coordination and context sharing

### **Tool Integration**  
- **Before**: Custom tool framework with manual validation
- **After**: ADK tools with automatic type checking and documentation
- **Benefit**: Better error handling and built-in Google ecosystem tools

### **Django Integration**
- **Before**: Direct model access scattered throughout agents
- **After**: Centralized Django integration layer
- **Benefit**: Better separation of concerns and easier testing

### **Development Experience**
- **Before**: Custom testing and debugging
- **After**: Built-in ADK web UI and evaluation tools
- **Benefit**: Rich development environment with session management

### **Deployment**
- **Before**: Custom Django views and API endpoints
- **After**: ADK built-in web server and Cloud deployment options
- **Benefit**: Production-ready deployment with scaling options

## 📊 Feature Comparison

| Feature | Current System | ADK System |
|---------|---------------|------------|
| Agent Definition | Custom Python classes | Declarative Agent() objects |
| Tool System | Manual BaseAgent.generate_payload() | Type-safe function tools |
| Multi-Agent | Manual routing in orchestrator | Native sub_agents support |
| Memory/Sessions | Custom implementation | Built-in session management |
| Development UI | None | Rich web UI with debugging |
| Evaluation | Custom tests | Built-in evaluation framework |
| Deployment | Django views | ADK web server + Cloud options |
| Google Integration | Manual API calls | Native Google tools |

## 🔄 Migration Steps

### Phase 1: Parallel Testing (Current)
- ✅ ADK system implemented alongside current system
- ✅ Django integration layer created
- ✅ Basic testing completed
- 🎯 **Next**: Set up API key and test with real data

### Phase 2: Frontend Integration
- Update frontend to use ADK endpoints instead of Django views
- Test message format compatibility
- Ensure all existing features work

### Phase 3: Production Migration
- Switch API endpoints to ADK system
- Monitor performance and functionality
- Retire old `agents/` directory

### Phase 4: Enhanced Features
- Leverage ADK evaluation framework
- Add Google ecosystem tools (BigQuery, etc.)
- Implement Cloud deployment

## 🛠 Technical Details

### Agent Structure Mapping

**Current Agent:**
```python
class OnboardingAgent(BaseAgent):
    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        return Message.TEXT, payload
```

**ADK Agent:**
```python
onboarding_agent = Agent(
    model='gemini-2.0-flash-001',
    name='onboarding_agent',
    instruction='...',
    tools=[get_user_account_balances, get_user_transactions]
)
```

### Tool Migration

**Current Tool (in BaseAgent):**
```python
def generate_payload(self, text: str) -> Dict:
    # Manual LLM call with litellm
    response = litellm.completion(...)
    return json.loads(response)
```

**ADK Tool:**
```python
def get_user_transactions(user_id: str, date_range: str = None) -> str:
    """Get user transactions from database."""
    # Direct Django model access
    return json.dumps(result)
```

### Django Integration

**Before**: Direct model access in each agent
**After**: Centralized integration layer with clear API:

```python
from agents_adk.django_integration import (
    get_user_transactions,
    get_user_account_balances,
    categorize_user_transaction,
    create_user_goal,
    generate_user_report
)
```

## 🎮 Usage Examples

### Interactive CLI
```bash
adk run agents_adk
# > Hello, I need help with my finances
# > Show me my spending report for last month
# > Create a goal to save $5000 for vacation
```

### Web UI
```bash
adk web agents_adk
# Opens http://localhost:8000 with full development interface
```

### Programmatic Usage
```python
from agents_adk.agent import root_agent

# Use the orchestrator
response = await root_agent.run("What's my net worth?")
```

## 🚨 Breaking Changes

1. **API Endpoints**: Will need to update frontend to use ADK endpoints
2. **Message Format**: ADK uses different message structures (but compatible)
3. **Tool Signatures**: New tool functions have different signatures
4. **Configuration**: Uses .env instead of Django settings for some configs

## 🔍 Troubleshooting

### Common Issues

**Import Errors**:
```bash
# Ensure Django is set up properly
export DJANGO_SETTINGS_MODULE=finance.settings
```

**API Key Issues**:
```bash
# Check .env file
cat agents_adk/.env
# Should contain: GOOGLE_API_KEY=your_key_here
```

**Tool Errors**:
```bash
# Test Django integration separately
python -c "from agents_adk.django_integration import get_user_transactions; print('OK')"
```

## 📈 Next Steps

1. **Set up API key** and test with real user data
2. **Update frontend** to use ADK endpoints
3. **Add evaluation sets** for testing agent performance
4. **Explore Google tools** for enhanced functionality
5. **Plan Cloud deployment** using ADK's built-in options

## 🎉 Benefits Summary

- ✅ **Better Architecture**: Native multi-agent support
- ✅ **Rich Development**: Built-in UI and debugging tools
- ✅ **Production Ready**: Cloud deployment and scaling
- ✅ **Google Ecosystem**: Native integration with Google services
- ✅ **Maintainability**: Cleaner code with less boilerplate
- ✅ **Future Proof**: Built on Google's agent framework 