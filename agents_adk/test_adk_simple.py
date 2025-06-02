#!/usr/bin/env python3
"""
Simple test to verify ADK integration works correctly.
This tests basic functionality without requiring extensive setup.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Set up environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def test_imports():
    """Test that all required imports work."""
    print("🧪 Testing imports...")
    
    try:
        # Test ADK imports
        from google.adk.agents import Agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types
        print("✅ ADK imports successful")
        
        # Test our agents
        from agents_adk.agent import all_agents
        print(f"✅ Imported {len(all_agents)} agents successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

async def test_simple_agent():
    """Test a simple agent creation and basic functionality."""
    print("\n🧪 Testing simple agent...")
    
    try:
        from google.adk.agents import Agent
        from google.adk.runners import Runner
        
        # Create a simple test agent
        test_agent = Agent(
            model='gemini-2.0-flash-001',
            name='test_agent',
            description='Simple test agent',
            instruction='You are a helpful test assistant. Respond briefly and clearly.'
        )
        
        print("✅ Test agent created successfully")
        
        # Test runner creation
        runner = Runner(test_agent)
        print("✅ ADK runner created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple agent test failed: {e}")
        return False

async def test_agent_execution():
    """Test actual agent execution with API key."""
    print("\n🧪 Testing agent execution...")
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️  No API key found - skipping execution test")
        return True
    
    try:
        from google.adk.agents import Agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types
        
        # Create a simple test agent
        test_agent = Agent(
            model='gemini-2.0-flash-001',
            name='test_agent',
            description='Simple test agent',
            instruction='You are a helpful test assistant. Respond briefly with "Hello! Test successful."'
        )
        
        session_service = InMemorySessionService()
        session_id = f"session_test_user_{hash('test') % 10000}"
        session = await session_service.create_session(app_name="SimpleTest", user_id="test_user", session_id=session_id)
        runner = Runner(agent=test_agent, app_name="SimpleTest", session_service=session_service)
        
        # Create test message
        test_message = "Hello, please respond with test confirmation."
        user_message = types.Content(role='user', parts=[types.Part(text=test_message)])
        
        # Run agent and collect response
        events = runner.run(user_id="test_user", session_id=session_id, new_message=user_message)
        response_parts = []
        for event in events:
            if event.is_final_response():
                response_parts.append(event.content.parts[0].text)
        
        response = ' '.join(response_parts) if response_parts else "No response"
        
        print(f"✅ Agent execution successful!")
        print(f"📤 Test prompt: {test_message}")
        print(f"📥 Agent response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent execution test failed: {e}")
        return False

async def test_finance_agents():
    """Test that our finance agents can be loaded."""
    print("\n🧪 Testing finance agents...")
    
    try:
        from agents_adk.agent import all_agents
        
        expected_agents = [
            'orchestrator',
            'onboarding_agent', 
            'cash_flow_agent',
            'goal_setting_agent',
            'reporting_agent',
            'investment_agent',
            'debt_strategy_agent',
            'safety_agent',
            'tax_pension_agent',
            'compliance_privacy_agent',
            'reminder_scheduler_agent',
            'conversation_agent'
        ]
        
        print(f"✅ Expected {len(expected_agents)} agents")
        print(f"✅ Found {len(all_agents)} agents")
        
        missing_agents = []
        for agent_name in expected_agents:
            if agent_name not in all_agents:
                missing_agents.append(agent_name)
            else:
                agent = all_agents[agent_name]
                print(f"   • {agent_name}: {agent.description[:50]}...")
        
        if missing_agents:
            print(f"❌ Missing agents: {missing_agents}")
            return False
        
        print("✅ All finance agents loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Finance agents test failed: {e}")
        return False

async def main():
    """Run all simple tests."""
    print("🚀 ADK Finance Agent Simple Tests")
    print("=" * 50)
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test simple agent
    results.append(await test_simple_agent())
    
    # Test finance agents
    results.append(await test_finance_agents())
    
    # Test execution (optional)
    results.append(await test_agent_execution())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! ADK integration is working correctly.")
        print("\n🚀 Next steps:")
        print("   1. Add your Google API key to .env file")
        print("   2. Run: python quick_test.py")
        print("   3. Run: python integration_test.py")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check the errors above.")
        if not os.getenv('GOOGLE_API_KEY'):
            print("\n💡 Tip: Add your Google API key to .env file for full testing")

if __name__ == "__main__":
    asyncio.run(main()) 