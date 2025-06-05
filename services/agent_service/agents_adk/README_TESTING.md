⚠️ **Cost Efficiency & Test Appropriateness Notice**

Before running any tests, always consider cost efficiency. Only execute the relevant tests if you have made changes to agent code or prompts. Avoid running unnecessary or broad test suites when your changes do not affect agent logic or prompt content.

# ADK Finance Agent Testing Guide

This guide covers all the different ways to test and interact with the ADK Finance Agent system.

## 🚀 Quick Start

1. **Set up your API key:**
   ```bash
   cp env_template .env
   # Edit .env and add your Google API key
   ```

2. **Choose your testing approach:**
   - `demo_agents.py` - See what each agent does (no API key needed)
   - `quick_test.py` - Interactive testing of individual agents
   - `integration_test.py` - Comprehensive testing of all agents
   - `test_adk.py` - Unit tests for system components

## 📋 Testing Scripts Overview

### 1. Demo Script (No API Key Required)
```bash
python demo_agents.py
```

**Purpose**: Understand what each agent does without making API calls
- Shows all 12 agents and their capabilities
- Lists example scenarios for each agent
- Explains tools and key features
- Perfect for initial exploration

### 2. Quick Interactive Testing
```bash
python quick_test.py
```

**Purpose**: Test individual agents with custom prompts
- Choose any agent from a menu
- Enter custom prompts
- See real API responses
- Perfect for exploring specific agent capabilities

**Features**:
- Interactive agent selection
- Custom prompt input
- Real-time testing
- Easy agent switching

### 3. Comprehensive Integration Testing
```bash
python integration_test.py
```

**Purpose**: Complete system testing with predefined scenarios
- Tests all 12 agents with realistic scenarios
- Tests multi-agent coordination
- Tests workflow system
- Generates detailed results report

**What it tests**:
- ✅ Orchestrator routing (8 scenarios)
- ✅ Individual agent capabilities (30+ scenarios)
- ✅ Multi-agent coordination (3 complex scenarios)
- ✅ Workflow system (4 workflows)
- ✅ Error handling and recovery

**Output**:
- Formatted console output with all responses
- JSON results file with detailed metrics
- Success/failure statistics
- Performance insights

### 4. Unit Testing
```bash
python test_adk.py
```

**Purpose**: Validate system components and structure
- Tests modular structure
- Validates agent creation
- Checks tool configuration
- Tests Django integration
- Validates workflows and state management

## 🤖 Agent Testing Scenarios

### Orchestrator Agent
Tests the main coordinator's ability to route requests appropriately:
```
- "I'm new to finance and want to get started tracking my money"
- "Help me create a budget for next month"
- "I want to set a goal to save $10,000 for a vacation"
- "Show me a report of my spending last month"
```

### Onboarding Agent
Tests new user setup and guidance:
```
- "I'm completely new to personal finance. Where do I start?"
- "I have bank accounts but have never tracked my spending"
- "What information do I need to provide to get a complete picture?"
```

### Cash Flow Agent
Tests budgeting and transaction management:
```
- "I spend about $3000/month but don't know where it goes"
- "I want to reduce my spending by $500/month"
- "How do I categorize transactions like 'Amazon' and 'Uber'?"
```

### Goal Setting Agent
Tests SMART goal creation and tracking:
```
- "I want to save for a house down payment. I can save $800/month and need $50,000"
- "Help me set up an emergency fund. I make $5,000/month"
- "Create a retirement savings goal for someone who's 35 years old"
```

### Investment Agent
Tests portfolio guidance and investment education:
```
- "I'm 30 years old with $10,000 to invest. What should I do?"
- "Explain the difference between a 401k and a Roth IRA"
- "I have $100,000 invested but it's all in my company stock. Is this risky?"
```

### Debt Strategy Agent
Tests debt payoff planning and strategies:
```
- "I have 3 credit cards: $5,000 at 18%, $3,000 at 22%, and $8,000 at 15%"
- "Should I pay off debt or invest? I have $2,000/month extra"
- "Help me create a debt avalanche plan for my credit cards"
```

### Reporting Agent
Tests financial analysis and reporting:
```
- "Create a monthly spending report template"
- "I want to analyze my spending trends. What metrics matter most?"
- "Generate a net worth tracking report format"
```

### Safety Agent
Tests security guidance and fraud prevention:
```
- "What are the most common financial scams I should watch out for?"
- "How do I protect my bank accounts and credit cards from fraud?"
- "I received a suspicious email about my bank account. What should I do?"
```

### Tax & Pension Agent
Tests tax planning and retirement guidance:
```
- "I'm self-employed. What tax strategies can help me save money?"
- "Explain the difference between traditional and Roth retirement accounts"
- "What are the 2024 contribution limits for 401k and IRA accounts?"
```

### Conversation Agent
Tests natural dialogue and emotional support:
```
- "I'm feeling overwhelmed by my finances. Where do I even begin?"
- "I tried budgeting before but I always give up. Any tips?"
- "Money stress is affecting my sleep. How do I deal with financial anxiety?"
```

## 🔄 Multi-Agent Coordination Tests

Tests how agents work together on complex scenarios:

### Complex Scenario 1: Young Professional
```
"I'm 28, make $80k/year, have $25k in student loans at 4.5%, 
$5k in credit card debt at 19%, and want to buy a house in 3 years. 
Create a comprehensive financial plan."
```

### Complex Scenario 2: Newlyweds
```
"I just got married and we're combining finances. We have different 
spending habits and conflicting financial goals. Help us create a unified strategy."
```

### Complex Scenario 3: Mid-Life Planning
```
"I'm 50 years old, behind on retirement savings, have aging parents 
who might need financial help, and a teenager heading to college. 
What's my priority order?"
```

## 📊 Results and Metrics

### Integration Test Results
After running `integration_test.py`, you'll get:

**Console Output**:
- Real-time test execution
- Formatted agent responses
- Error handling demonstrations
- Progress indicators

**JSON Results File** (`integration_test_results.json`):
```json
{
  "timestamp": "2024-06-02T19:44:08",
  "summary": {
    "total_tests": 45,
    "successful_tests": 42,
    "success_rate": 93.3
  },
  "detailed_results": {
    "orchestrator_test_1": {
      "prompt": "I'm new to finance...",
      "response": "Welcome to personal finance...",
      "success": true
    }
  }
}
```

### Key Metrics Tracked
- **Response Quality**: Relevance and helpfulness of agent responses
- **Agent Coordination**: How well agents work together
- **Error Handling**: Graceful handling of issues
- **Performance**: Response times and system stability

## 🛠 Development Testing

### ADK CLI Testing
```bash
# Interactive CLI interface
adk run agents_adk

# Web development UI
adk web agents_adk
```

### Django Integration Testing
The tests verify:
- Database connectivity
- Model access and queries
- Transaction handling
- Error management
- Data security

### Workflow Testing
Tests the four main workflows:
- **Onboarding**: New user setup process
- **Budget Creation**: Comprehensive budget planning
- **Goal Tracking**: Progress monitoring and optimization
- **Financial Health Check**: Complete financial assessment

## 🚨 Troubleshooting

### Common Issues

**API Key Problems**:
```bash
# Check if .env file exists
ls -la .env

# Verify API key format
cat .env | grep GOOGLE_API_KEY
```

**Import Errors**:
```bash
# Ensure Django setup
export DJANGO_SETTINGS_MODULE=finance.settings

# Check Python path
python -c "import sys; print(sys.path)"
```

**Agent Response Issues**:
- Check API key validity
- Verify internet connection
- Review prompt formatting
- Check rate limiting

**Django Integration Issues**:
```bash
# Test Django separately
python manage.py shell
>>> from myFinance.models import Transaction
>>> print("Django OK")
```

## 📈 Performance Guidelines

### Expected Response Times
- Simple queries: 2-5 seconds
- Complex coordination: 5-15 seconds
- Workflow execution: 10-30 seconds

### Rate Limiting
- Google API has rate limits
- Integration tests include delays
- Use quick_test.py for rapid iteration

## 🎯 Best Practices

### Testing Strategy
1. **Start with demo_agents.py** to understand capabilities
2. **Use quick_test.py** for focused testing
3. **Run integration_test.py** for comprehensive validation
4. **Use test_adk.py** for system validation

### Prompt Engineering
- Be specific about financial situations
- Include relevant numbers and context
- Test edge cases and error scenarios
- Validate agent routing and coordination

### Result Analysis
- Review response quality and relevance
- Check for proper agent coordination
- Validate tool usage and data access
- Monitor error handling and recovery

## 🔄 Continuous Testing

### Pre-Production Checklist
- [ ] All unit tests passing
- [ ] Integration tests >90% success rate
- [ ] All agents responding appropriately
- [ ] Multi-agent coordination working
- [ ] Workflows executing correctly
- [ ] Django integration functional
- [ ] Error handling graceful
- [ ] Performance within guidelines

### Monitoring Recommendations
- Track agent response quality
- Monitor API usage and costs
- Validate user satisfaction
- Check system performance
- Review error rates and patterns

---

## 🎉 Ready to Test!

Choose your testing approach and start exploring the ADK Finance Agent system:

1. **Demo first**: `python demo_agents.py`
2. **Quick test**: `python quick_test.py`
3. **Full test**: `python integration_test.py`
4. **System check**: `python test_adk.py`

The system is ready for comprehensive testing and evaluation! 