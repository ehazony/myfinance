#!/usr/bin/env python3
"""
Quick interactive test script for individual agents.
Allows you to test specific agents with custom prompts.

Usage:
python quick_test.py
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

from ..agents_adk.agent import all_agents

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
        # Create session service and session
        session_service = InMemorySessionService()
        session_id = f"session_{user_id}_{hash(prompt) % 10000}"
        session = await session_service.create_session(app_name="FinanceAgentTest", user_id=user_id, session_id=session_id)
        
        # Create runner
        runner = Runner(agent=agent, app_name="FinanceAgentTest", session_service=session_service)
        
        # Create user message with the actual prompt and role
        user_message = types.Content(role='user', parts=[types.Part(text=prompt)])
        
        # Run agent and collect response
        events = runner.run(user_id=user_id, session_id=session_id, new_message=user_message)
        
        # Process events to get final response
        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                return final_response
        
        return f"Agent {agent.name} processed the request but didn't generate a final response."
        
    except Exception as e:
        error_msg = str(e)
        
        # Provide more helpful error messages for common issues
        if "function calling is unsupported" in error_msg:
            return f"Agent {agent.name} uses tools that aren't currently supported in this demo environment. Try the simple_ version of this agent instead."
        elif "Default value" in error_msg and "parameter annotation" in error_msg:
            return f"Agent {agent.name} has tool configuration issues. This is a known limitation with some finance tools."
        elif "400 INVALID_ARGUMENT" in error_msg:
            return f"Agent {agent.name} encountered an API limitation with tool usage."
        else:
            return f"Error executing agent {agent.name}: {error_msg}"


async def test_agent_interactive():
    """Interactive agent testing."""
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found!")
        print("Please add your API key to the .env file.")
        return
    
    print("🚀 ADK Finance Agent Quick Test")
    print("=" * 50)
    print(f"✅ API key loaded: {api_key[:20]}...")
    
    # Show available agents
    print("\n🤖 Available Agents:")
    for i, (name, agent) in enumerate(all_agents.items(), 1):
        print(f"  {i:2d}. {name} - {agent.description}")
    
    while True:
        try:
            print("\n" + "=" * 50)
            choice = input("\nSelect an agent (number) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                break
            
            try:
                agent_index = int(choice) - 1
                agent_names = list(all_agents.keys())
                if 0 <= agent_index < len(agent_names):
                    agent_name = agent_names[agent_index]
                    agent = all_agents[agent_name]
                else:
                    print("❌ Invalid agent number!")
                    continue
            except ValueError:
                print("❌ Please enter a valid number!")
                continue
            
            print(f"\n🤖 Testing: {agent_name}")
            print(f"📝 Description: {agent.description}")
            
            prompt = input("\n💬 Enter your prompt (or 'back' to choose another agent): ").strip()
            
            if prompt.lower() == 'back':
                continue
            
            if not prompt:
                print("❌ Please enter a prompt!")
                continue
            
            print(f"\n🔄 Processing with {agent_name}...")
            print("-" * 50)
            
            try:
                response = await run_agent_with_prompt(agent, prompt)
                print(f"\n💡 Response from {agent_name}:")
                print("=" * 50)
                print(response)
                print("=" * 50)
            except Exception as e:
                print(f"❌ Error: {e}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


async def run_quick_examples():
    """Run a few quick examples to demonstrate each agent."""
    
    print("🎯 Quick Agent Demonstrations")
    print("=" * 50)
    
    # Use simple agents without tools for reliable demonstration
    examples = [
        ("simple_investment_agent", "I'm 30 years old with $50,000 to invest. I have an emergency fund already. What's your recommendation?"),
        ("simple_safety_agent", "What are the most important financial security tips I should implement immediately?"),
        ("simple_tax_pension_agent", "I'm choosing between contributing to my company's 401k or opening a Roth IRA. Which should I choose?"),
        ("onboarding_agent", "I'm completely new to personal finance and feel overwhelmed. Where should I start?"),
        ("cash_flow_agent", "I need help creating my first monthly budget. What's the best approach?"),
        ("goal_setting_agent", "I want to save $20,000 for a house down payment in 2 years. How do I make this realistic?"),
        ("debt_strategy_agent", "I have $10,000 in credit card debt at 18% interest. What's the best strategy to pay it off?"),
        ("conversation_agent", "I'm really stressed about money and don't know where to begin organizing my finances.")
    ]
    
    for agent_name, prompt in examples:
        try:
            print(f"\n🤖 {agent_name.upper()}")
            print(f"📝 Prompt: {prompt}")
            print("-" * 40)
            
            if agent_name not in all_agents:
                print(f"❌ Agent {agent_name} not found")
                continue
                
            agent = all_agents[agent_name]
            response = await run_agent_with_prompt(agent, prompt)
            
            # Show more of the response for better demonstration
            if len(response) > 500:
                response = response[:500] + "..."
            
            print(f"💬 Response: {response}")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error with {agent_name}: {e}")
            # Continue with other agents instead of stopping


async def main():
    """Main function to choose test mode."""
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found!")
        print("Please add your API key to the .env file.")
        return
    
    print("🚀 ADK Finance Agent Quick Test")
    print("=" * 50)
    print("Choose test mode:")
    print("1. Interactive testing (choose agents and prompts)")
    print("2. Quick examples (see all agents in action)")
    
    choice = input("\nEnter 1 or 2: ").strip()
    
    if choice == "1":
        await test_agent_interactive()
    elif choice == "2":
        await run_quick_examples()
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    asyncio.run(main()) 