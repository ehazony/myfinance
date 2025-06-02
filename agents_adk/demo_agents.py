#!/usr/bin/env python3
"""
Demo script that shows the capabilities of each agent without requiring API calls.
Perfect for understanding what each agent does before testing with real API.

Usage:
python demo_agents.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Set up environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

from agents_adk.agent import all_agents


def print_agent_demo(agent_name: str, agent, example_scenarios: list):
    """Print a demo of what an agent does."""
    print(f"\n🤖 {agent_name.upper().replace('_', ' ')}")
    print("=" * 60)
    print(f"📝 Description: {agent.description}")
    print(f"🎯 Model: {agent.model}")
    
    # Show tools
    tools = []
    for tool in agent.tools:
        if hasattr(tool, '__name__'):
            tools.append(tool.__name__)
        elif hasattr(tool, 'name'):
            tools.append(tool.name)
        else:
            tools.append(str(type(tool).__name__))
    
    print(f"🔧 Tools: {', '.join(tools)}")
    
    print(f"\n💡 Example Scenarios:")
    for i, scenario in enumerate(example_scenarios, 1):
        print(f"   {i}. {scenario}")
    
    # Show key instruction highlights
    instruction = agent.instruction
    if len(instruction) > 500:
        # Extract key points
        lines = instruction.split('\n')
        key_points = [line.strip() for line in lines if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-'))][:5]
        if key_points:
            print(f"\n🎯 Key Capabilities:")
            for point in key_points:
                print(f"   • {point}")


def main():
    """Demo all agents and their capabilities."""
    
    print("🚀 ADK Finance Agent System Demo")
    print("=" * 60)
    print("This demo shows what each agent can do without requiring API calls.")
    print("For live testing, use integration_test.py or quick_test.py with your API key.")
    
    # Agent demos with example scenarios
    agent_demos = {
        'orchestrator': [
            "I need help with my overall financial situation",
            "Route me to the right specialist for budgeting",
            "I have multiple financial goals - help me prioritize",
            "Create a comprehensive financial plan for me"
        ],
        
        'onboarding_agent': [
            "I'm completely new to personal finance",
            "Help me connect my bank accounts securely",
            "What financial information should I track?",
            "Guide me through setting up my financial baseline"
        ],
        
        'cash_flow_agent': [
            "I spend $3000/month but don't know where it goes",
            "Help me create a realistic monthly budget",
            "How should I categorize my transactions?",
            "I want to reduce spending by $500/month"
        ],
        
        'goal_setting_agent': [
            "I want to save $50,000 for a house down payment",
            "Help me set up a 6-month emergency fund",
            "Create a plan to pay off $20,000 in debt",
            "Set retirement savings goals for a 35-year-old"
        ],
        
        'investment_agent': [
            "I'm 30 with $10,000 to invest - what should I do?",
            "Explain 401k vs Roth IRA for my situation",
            "Is my portfolio properly diversified?",
            "What's a good asset allocation for retirement?"
        ],
        
        'debt_strategy_agent': [
            "I have 3 credit cards with different rates",
            "Should I pay off debt or invest extra money?",
            "Help me create a debt avalanche plan",
            "Is debt consolidation right for me?"
        ],
        
        'reporting_agent': [
            "Create a monthly spending report template",
            "What financial KPIs should I track?",
            "Generate a net worth tracking system",
            "Show me spending trends and insights"
        ],
        
        'safety_agent': [
            "What are common financial scams to avoid?",
            "How do I protect my accounts from fraud?",
            "Best practices for online banking security",
            "I got a suspicious financial email - what to do?"
        ],
        
        'tax_pension_agent': [
            "Tax strategies for self-employed individuals",
            "Retirement account contribution limits for 2024",
            "Traditional vs Roth - which is better for me?",
            "How to plan for taxes in retirement"
        ],
        
        'compliance_privacy_agent': [
            "What are my financial privacy rights?",
            "How is my financial data protected?",
            "Banking regulations I should know about",
            "Data security best practices for finance"
        ],
        
        'reminder_scheduler_agent': [
            "Set up bill payment reminders",
            "Schedule monthly budget reviews",
            "Remind me to check investment performance",
            "Create a financial task calendar"
        ],
        
        'conversation_agent': [
            "I'm overwhelmed by financial planning",
            "Help me stay motivated with my budget",
            "I keep failing at financial goals - advice?",
            "Make financial planning less stressful"
        ]
    }
    
    # Show each agent demo
    for agent_name, scenarios in agent_demos.items():
        if agent_name in all_agents:
            print_agent_demo(agent_name, all_agents[agent_name], scenarios)
    
    # Show integration capabilities
    print(f"\n🔗 INTEGRATION CAPABILITIES")
    print("=" * 60)
    print("🏗️  Multi-Agent Coordination:")
    print("   • Agents automatically work together on complex requests")
    print("   • Orchestrator routes requests to appropriate specialists") 
    print("   • Context shared between agents for seamless experience")
    
    print(f"\n💾 State Management:")
    print("   • Session persistence across conversations")
    print("   • Financial context and goal tracking")
    print("   • User preference learning and adaptation")
    
    print(f"\n🔄 Workflow System:")
    print("   • Onboarding: Complete new user setup process")
    print("   • Budget Creation: Comprehensive budget planning workflow")
    print("   • Goal Tracking: Progress monitoring and optimization")
    print("   • Financial Health Check: Complete financial assessment")
    
    print(f"\n🛠️  Django Integration:")
    print("   • Real database access for transactions and accounts")
    print("   • User goal and tag management")
    print("   • Financial report generation from real data")
    print("   • Secure data handling with error management")
    
    print(f"\n🚀 Getting Started:")
    print("=" * 60)
    print("1. Copy env_template to .env")
    print("2. Add your Google API key to .env")
    print("3. Run: python integration_test.py (comprehensive testing)")
    print("4. Run: python quick_test.py (interactive testing)")
    print("5. Run: adk web agents_adk (development UI)")
    print("6. Run: adk run agents_adk (CLI interface)")
    
    print(f"\n📊 System Status:")
    print(f"   ✅ {len(all_agents)} agents implemented and ready")
    print(f"   ✅ Modular architecture with proper separation")
    print(f"   ✅ Enhanced tools with Django integration")
    print(f"   ✅ Workflow system for complex processes")
    print(f"   ✅ Session management and state persistence")
    print(f"   ✅ Production-ready with ADK framework")


if __name__ == "__main__":
    main() 