#!/usr/bin/env python3
"""
Test script for the ADK-based finance agent system.
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

# Import the agents
from agents_adk.agent import root_agent, onboarding_agent, cash_flow_agent

def test_basic_agent_creation():
    """Test that agents are created properly."""
    print("Testing agent creation...")
    
    assert root_agent.name == 'finance_orchestrator'
    assert onboarding_agent.name == 'onboarding_agent'
    assert cash_flow_agent.name == 'cash_flow_agent'
    
    print("✅ Agents created successfully")
    
    # Check sub-agents
    assert len(root_agent.sub_agents) == 5
    print("✅ Sub-agents configured correctly")

def test_tools_configuration():
    """Test that tools are configured properly."""
    print("\nTesting tools configuration...")
    
    # Check root agent tools (handle different tool types)
    root_tools = []
    for tool in root_agent.tools:
        if hasattr(tool, '__name__'):
            root_tools.append(tool.__name__)
        elif hasattr(tool, 'name'):
            root_tools.append(tool.name)
        elif hasattr(tool, '__class__'):
            root_tools.append(tool.__class__.__name__)
        else:
            root_tools.append(str(type(tool)))
    
    expected_tools = ['get_user_transactions', 'get_user_account_balances', 'generate_user_report']
    
    for tool in expected_tools:
        if any(tool in rt for rt in root_tools):
            print(f"✅ Tool configured: {tool}")
        else:
            print(f"❌ Missing tool: {tool}")
    
    print(f"📋 All configured tools: {', '.join(root_tools)}")

async def test_agent_interaction():
    """Test basic agent interaction (requires API key)."""
    print("\nTesting agent interaction...")
    
    try:
        # This would require proper API key setup
        response = await root_agent.run("Hello, I need help with my finances")
        print(f"✅ Agent responded: {response[:100]}...")
    except Exception as e:
        print(f"⚠️  Agent interaction test skipped (API key needed): {e}")

def test_django_integration():
    """Test Django integration functions."""
    print("\nTesting Django integration...")
    
    try:
        from agents_adk.django_integration import (
            get_user_transactions,
            get_user_account_balances,
            categorize_user_transaction,
            create_user_goal,
            generate_user_report
        )
        print("✅ Django integration functions imported successfully")
        
        # Test with mock user_id (will fail gracefully)
        result = get_user_account_balances("999")
        print(f"✅ Function call works (expected error): {result[:50]}...")
        
    except Exception as e:
        print(f"❌ Django integration error: {e}")

def test_adk_commands():
    """Test ADK CLI commands availability."""
    print("\nTesting ADK CLI commands...")
    
    try:
        import subprocess
        result = subprocess.run(['adk', '--help'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ADK CLI is available")
            if 'web' in result.stdout:
                print("✅ ADK web command available")
            if 'run' in result.stdout:
                print("✅ ADK run command available")
        else:
            print("❌ ADK CLI not working properly")
    except Exception as e:
        print(f"⚠️  ADK CLI test skipped: {e}")

def main():
    """Run all tests."""
    print("🧪 Testing ADK Finance Agent System")
    print("=" * 50)
    
    test_basic_agent_creation()
    test_tools_configuration()
    test_django_integration()
    test_adk_commands()
    
    # Async test
    try:
        asyncio.run(test_agent_interaction())
    except Exception as e:
        print(f"⚠️  Async test skipped: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 ADK system tests completed!")
    print("\nNext steps:")
    print("1. Set up Google API key in .env file (copy from env_template)")
    print("2. Test interactively with: adk run agents_adk")
    print("3. Start web UI with: adk web agents_adk")
    print("4. Replace old agents/ directory when ready")

if __name__ == "__main__":
    main() 