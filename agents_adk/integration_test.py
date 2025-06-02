#!/usr/bin/env python3
"""
Integration tests for ADK Finance Agent System with real API calls.
This script demonstrates each agent's capabilities using actual API keys.

Setup:
1. Copy env_template to .env
2. Add your Google API key to .env
3. Run: python integration_test.py
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Set up environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    print(f"📁 Loading environment from: {env_file}")
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
else:
    print("⚠️  No .env file found. Please copy env_template to .env and add your API key.")
    sys.exit(1)

# Import agents after environment setup
from agents_adk.agent import all_agents, finance_workflows

# Import ADK components for proper execution
try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
except ImportError as e:
    print(f"❌ ADK import error: {e}")
    print("Please ensure google-adk is installed: pip install google-adk")
    sys.exit(1)


async def run_agent_with_prompt(agent, prompt: str, user_id: str = "test_user"):
    """Run an agent with a prompt using proper ADK runner."""
    try:
        session_service = InMemorySessionService()
        session_id = f"session_{user_id}_{hash(prompt) % 10000}"
        session = await session_service.create_session(app_name="IntegrationTest", user_id=user_id, session_id=session_id)
        runner = Runner(agent=agent, app_name="IntegrationTest", session_service=session_service)
        user_message = types.Content(role='user', parts=[types.Part(text=prompt)])
        events = runner.run(user_id=user_id, session_id=session_id, new_message=user_message)
        for event in events:
            if event.is_final_response():
                return event.content.parts[0].text
        return f"Agent {agent.name} processed the request but didn't generate a final response."
    except Exception as e:
        return f"Error executing agent: {e}"


class AgentTester:
    """Comprehensive agent testing with real API calls."""
    
    def __init__(self):
        self.agents = all_agents
        self.workflows = finance_workflows
        self.test_user_id = "integration_test_user"
        self.results = {}
    
    def print_header(self, title: str):
        """Print formatted section header."""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print('='*60)
    
    def print_result(self, agent_name: str, prompt: str, response: str):
        """Print formatted test result."""
        print(f"\n🤖 Agent: {agent_name}")
        print(f"📝 Prompt: {prompt}")
        print(f"💬 Response: {response}")
        print("-" * 40)
    
    async def test_orchestrator_routing(self):
        """Test the main orchestrator's ability to route requests."""
        self.print_header("ORCHESTRATOR ROUTING TESTS")
        
        test_scenarios = [
            "I'm new to finance and want to get started tracking my money",
            "Help me create a budget for next month",
            "I want to set a goal to save $10,000 for a vacation",
            "Show me a report of my spending last month", 
            "I need help paying off my credit card debt",
            "What's the best way to invest for retirement?",
            "I'm worried about financial scams, what should I know?",
            "Help me plan for taxes this year"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            try:
                print(f"\n🔄 Test {i}/8: {scenario}")
                response = await run_agent_with_prompt(self.agents['orchestrator'], scenario, self.test_user_id)
                self.print_result('orchestrator', scenario, response)
                self.results[f'orchestrator_test_{i}'] = {
                    'prompt': scenario,
                    'response': response,
                    'success': True
                }
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results[f'orchestrator_test_{i}'] = {
                    'prompt': scenario,
                    'error': str(e),
                    'success': False
                }
    
    async def test_onboarding_agent(self):
        """Test the onboarding agent's capabilities."""
        self.print_header("ONBOARDING AGENT TESTS")
        
        scenarios = [
            "I'm completely new to personal finance. Where do I start?",
            "I have bank accounts but have never tracked my spending. Help me get organized.",
            "What information do I need to provide to get a complete financial picture?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['onboarding_agent'], scenario, self.test_user_id)
                self.print_result('onboarding_agent', scenario, response)
            except Exception as e:
                print(f"❌ Onboarding agent error: {e}")
    
    async def test_cash_flow_agent(self):
        """Test the cash flow agent's budgeting capabilities."""
        self.print_header("CASH FLOW AGENT TESTS")
        
        scenarios = [
            "I spend about $3000/month but don't know where it goes. Help me create a budget.",
            "I want to reduce my spending by $500/month. Where should I look?",
            "How do I categorize transactions like 'Amazon' and 'Uber'?",
            "My income varies each month. How do I budget for irregular income?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['cash_flow_agent'], scenario, self.test_user_id)
                self.print_result('cash_flow_agent', scenario, response)
            except Exception as e:
                print(f"❌ Cash flow agent error: {e}")
    
    async def test_goal_setting_agent(self):
        """Test the goal setting agent's SMART goal capabilities."""
        self.print_header("GOAL SETTING AGENT TESTS")
        
        scenarios = [
            "I want to save for a house down payment. I can save $800/month and need $50,000.",
            "Help me set up an emergency fund. I make $5,000/month.",
            "I want to pay off $15,000 in credit card debt as quickly as possible.",
            "Create a retirement savings goal for someone who's 35 years old."
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['goal_setting_agent'], scenario, self.test_user_id)
                self.print_result('goal_setting_agent', scenario, response)
            except Exception as e:
                print(f"❌ Goal setting agent error: {e}")
    
    async def test_investment_agent(self):
        """Test the investment agent's portfolio guidance."""
        self.print_header("INVESTMENT AGENT TESTS")
        
        scenarios = [
            "I'm 30 years old with $10,000 to invest. What should I do?",
            "Explain the difference between a 401k and a Roth IRA for someone making $75,000/year.",
            "I have $100,000 invested but it's all in my company stock. Is this risky?",
            "What's a good asset allocation for someone 10 years from retirement?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['investment_agent'], scenario, self.test_user_id)
                self.print_result('investment_agent', scenario, response)
            except Exception as e:
                print(f"❌ Investment agent error: {e}")
    
    async def test_debt_strategy_agent(self):
        """Test the debt strategy agent's payoff planning."""
        self.print_header("DEBT STRATEGY AGENT TESTS")
        
        scenarios = [
            "I have 3 credit cards: $5,000 at 18%, $3,000 at 22%, and $8,000 at 15%. What's the best payoff strategy?",
            "Should I pay off debt or invest? I have $2,000/month extra and 6% student loans.",
            "I'm considering debt consolidation. What should I know?",
            "Help me create a debt avalanche plan for my credit cards."
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['debt_strategy_agent'], scenario, self.test_user_id)
                self.print_result('debt_strategy_agent', scenario, response)
            except Exception as e:
                print(f"❌ Debt strategy agent error: {e}")
    
    async def test_reporting_agent(self):
        """Test the reporting agent's analysis capabilities."""
        self.print_header("REPORTING AGENT TESTS")
        
        scenarios = [
            "Create a monthly spending report template. What categories should I track?",
            "I want to analyze my spending trends. What metrics matter most?",
            "Generate a net worth tracking report format for someone with multiple accounts.",
            "What key performance indicators should I monitor for my financial health?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['reporting_agent'], scenario, self.test_user_id)
                self.print_result('reporting_agent', scenario, response)
            except Exception as e:
                print(f"❌ Reporting agent error: {e}")
    
    async def test_safety_agent(self):
        """Test the safety agent's security guidance."""
        self.print_header("SAFETY AGENT TESTS")
        
        scenarios = [
            "What are the most common financial scams I should watch out for?",
            "How do I protect my bank accounts and credit cards from fraud?",
            "I received a suspicious email about my bank account. What should I do?",
            "What security measures should I use for online banking?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['safety_agent'], scenario, self.test_user_id)
                self.print_result('safety_agent', scenario, response)
            except Exception as e:
                print(f"❌ Safety agent error: {e}")
    
    async def test_tax_pension_agent(self):
        """Test the tax and pension planning agent."""
        self.print_header("TAX & PENSION AGENT TESTS")
        
        scenarios = [
            "I'm self-employed. What tax strategies can help me save money?",
            "Explain the difference between traditional and Roth retirement accounts.",
            "I'm 45 and haven't saved much for retirement. What should I do?",
            "What are the 2024 contribution limits for 401k and IRA accounts?"
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['tax_pension_agent'], scenario, self.test_user_id)
                self.print_result('tax_pension_agent', scenario, response)
            except Exception as e:
                print(f"❌ Tax pension agent error: {e}")
    
    async def test_conversation_agent(self):
        """Test the conversation agent's dialogue management."""
        self.print_header("CONVERSATION AGENT TESTS")
        
        scenarios = [
            "I'm feeling overwhelmed by my finances. Where do I even begin?",
            "I tried budgeting before but I always give up. Any tips?",
            "Money stress is affecting my sleep. How do I deal with financial anxiety?",
            "I want to get better with money but don't know my learning style. Help me find the right approach."
        ]
        
        for scenario in scenarios:
            try:
                response = await run_agent_with_prompt(self.agents['conversation_agent'], scenario, self.test_user_id)
                self.print_result('conversation_agent', scenario, response)
            except Exception as e:
                print(f"❌ Conversation agent error: {e}")
    
    async def test_multi_agent_coordination(self):
        """Test how agents work together on complex scenarios."""
        self.print_header("MULTI-AGENT COORDINATION TESTS")
        
        complex_scenarios = [
            "I'm 28, make $80k/year, have $25k in student loans at 4.5%, $5k in credit card debt at 19%, and want to buy a house in 3 years. Create a comprehensive financial plan.",
            "I just got married and we're combining finances. We have different spending habits and conflicting financial goals. Help us create a unified strategy.",
            "I'm 50 years old, behind on retirement savings, have aging parents who might need financial help, and a teenager heading to college. What's my priority order?"
        ]
        
        for scenario in complex_scenarios:
            try:
                print(f"\n🔄 Complex Scenario: {scenario}")
                response = await run_agent_with_prompt(self.agents['orchestrator'], scenario, self.test_user_id)
                self.print_result('orchestrator (multi-agent)', scenario, response)
            except Exception as e:
                print(f"❌ Multi-agent coordination error: {e}")
    
    async def test_workflows(self):
        """Test the workflow system."""
        self.print_header("WORKFLOW TESTS")
        
        try:
            # Test onboarding workflow
            print("\n🔄 Testing Onboarding Workflow...")
            onboarding_result = await self.workflows['onboarding'].run(
                user_id=self.test_user_id,
                initial_message="I want to start managing my finances"
            )
            print(f"✅ Onboarding workflow: {onboarding_result}")
            
            # Test budget creation workflow
            print("\n🔄 Testing Budget Creation Workflow...")
            budget_result = await self.workflows['budget_creation'].run(
                user_id=self.test_user_id,
                budget_period="monthly"
            )
            print(f"✅ Budget creation workflow: {budget_result}")
            
            # Test goal tracking workflow
            print("\n🔄 Testing Goal Tracking Workflow...")
            goal_result = await self.workflows['goal_tracking'].run(
                user_id=self.test_user_id
            )
            print(f"✅ Goal tracking workflow: {goal_result}")
            
        except Exception as e:
            print(f"❌ Workflow test error: {e}")
    
    def generate_summary_report(self):
        """Generate a summary of all test results."""
        self.print_header("INTEGRATION TEST SUMMARY")
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results.values() if r.get('success', False))
        
        print(f"📊 Test Results Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {total_tests - successful_tests}")
        print(f"   Success Rate: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "   Success Rate: N/A")
        
        # Show failed tests
        failed_tests = [name for name, result in self.results.items() if not result.get('success', False)]
        if failed_tests:
            print(f"\n❌ Failed Tests:")
            for test_name in failed_tests:
                print(f"   - {test_name}: {self.results[test_name].get('error', 'Unknown error')}")
        
        # Save detailed results
        results_file = Path(__file__).parent / 'integration_test_results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'success_rate': successful_tests/total_tests*100 if total_tests > 0 else 0
                },
                'detailed_results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")


async def main():
    """Run comprehensive integration tests."""
    print("🚀 Starting ADK Finance Agent Integration Tests")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment!")
        print("Please add your API key to the .env file.")
        return
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    tester = AgentTester()
    
    try:
        # Test individual agents
        await tester.test_orchestrator_routing()
        await tester.test_onboarding_agent()
        await tester.test_cash_flow_agent()
        await tester.test_goal_setting_agent()
        await tester.test_investment_agent()
        await tester.test_debt_strategy_agent()
        await tester.test_reporting_agent()
        await tester.test_safety_agent()
        await tester.test_tax_pension_agent()
        await tester.test_conversation_agent()
        
        # Test coordination and workflows
        await tester.test_multi_agent_coordination()
        await tester.test_workflows()
        
        # Generate summary
        tester.generate_summary_report()
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print(f"🔧 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌍 Environment variables loaded: {len(os.environ)}")
    
    asyncio.run(main()) 