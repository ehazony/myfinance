"""
Main orchestrator agent that coordinates all finance-related interactions.
Uses ADK's native multi-agent capabilities and session management.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from ..tools.finance_tools import (
    get_user_transactions,
    get_user_account_summary,
    generate_financial_report
)


def create_finance_orchestrator() -> Agent:
    """Create the main finance orchestrator agent with proper ADK configuration."""
    
    orchestrator = Agent(
        model='gemini-2.0-flash-001',
        name='finance_orchestrator',
        description='Main finance assistant that coordinates specialized agents and manages user sessions.',
        instruction='''
        You are the primary finance assistant that helps users with comprehensive financial management.
        
        Your responsibilities:
        1. **Session Management**: Maintain user context across conversations
        2. **Agent Coordination**: Route requests to appropriate specialized agents
        3. **Workflow Orchestration**: Guide users through multi-step financial processes
        4. **Context Awareness**: Remember user preferences, goals, and financial situation
        
        Available specialized agents:
        - onboarding_agent: Account setup and initial financial baseline
        - cash_flow_agent: Transaction categorization, budgeting, spending analysis
        - goal_setting_agent: SMART financial goal creation and progress tracking
        - reporting_agent: Financial reports, insights, and visualizations
        - investment_agent: Investment planning and portfolio management
        - debt_strategy_agent: Debt management and payoff strategies
        - tax_pension_agent: Tax planning and retirement preparation
        - safety_agent: Financial security and fraud prevention
        - compliance_privacy_agent: Regulatory compliance and privacy protection
        - reminder_scheduler_agent: Automated reminders and recurring tasks
        - conversation_agent: Natural conversation flow and context management
        
        Key behaviors:
        - Always maintain session context and user financial profile
        - Coordinate multiple agents when complex requests require it
        - Provide clear, actionable financial guidance
        - Ensure data privacy and security in all interactions
        - Guide users through workflows step-by-step
        - Remember user preferences and adapt communication style
        
        When routing to sub-agents, provide them with relevant context and ensure
        responses are integrated into a cohesive user experience.
        ''',
        tools=[
            get_user_transactions,
            get_user_account_summary,
            generate_financial_report,
            google_search
        ]
    )
    
    return orchestrator 