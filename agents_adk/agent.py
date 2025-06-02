import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.planners import PlanReActPlanner
from google.genai import types

# Import Django integration functions
from .django_integration import (
    get_user_transactions,
    get_user_account_balances,
    categorize_user_transaction,
    create_user_goal,
    generate_user_report
)

# Load environment variables
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

# Finance Domain Tools
def get_transactions(user_id: str, date_range: str = None) -> str:
    """Get user transactions from the database.
    
    Args:
        user_id: The user identifier
        date_range: Optional date range filter (e.g., "2024-01")
        
    Returns:
        JSON string of transaction data
    """
    # This would integrate with your Django models
    return f"Mock transactions for user {user_id} in range {date_range}"

def get_account_balance(user_id: str, account_type: str = None) -> str:
    """Get user account balances.
    
    Args:
        user_id: The user identifier
        account_type: Optional account type filter
        
    Returns:
        JSON string of account balance data
    """
    return f"Mock balance data for user {user_id}, account_type {account_type}"

def categorize_transaction(transaction_id: str, category: str) -> str:
    """Categorize a transaction.
    
    Args:
        transaction_id: The transaction identifier
        category: The category to assign
        
    Returns:
        Success message
    """
    return f"Transaction {transaction_id} categorized as {category}"

def create_budget_goal(user_id: str, category: str, amount: float, period: str) -> str:
    """Create a budget goal.
    
    Args:
        user_id: The user identifier
        category: Budget category
        amount: Budget amount
        period: Budget period (monthly, yearly, etc.)
        
    Returns:
        Success message with goal ID
    """
    return f"Budget goal created for {category}: ${amount}/{period}"

def generate_report(user_id: str, report_type: str, period: str) -> str:
    """Generate financial reports.
    
    Args:
        user_id: The user identifier
        report_type: Type of report (spending, income, net_worth, etc.)
        period: Report period
        
    Returns:
        Report data as JSON string
    """
    return f"Generated {report_type} report for {period}"

# Specialized Finance Agents
onboarding_agent = Agent(
    model='gemini-2.0-flash-001',
    name='onboarding_agent',
    description='Helps users connect accounts and set up their financial baseline.',
    instruction='''
    You help users onboard to the financial system by:
    1. Guiding them through account connection
    2. Explaining data import options  
    3. Setting up initial financial snapshots
    4. Ensuring account security and permissions
    Always be encouraging and explain the benefits of each step.
    ''',
    tools=[get_user_account_balances, get_user_transactions]
)

cash_flow_agent = Agent(
    model='gemini-2.0-flash-001',
    name='cash_flow_agent', 
    description='Manages transaction categorization and budget planning.',
    instruction='''
    You help users manage their cash flow by:
    1. Categorizing transactions automatically and manually
    2. Setting up budgets and spending goals
    3. Tracking spending patterns
    4. Providing budget alerts and recommendations
    Focus on practical, actionable advice for better money management.
    ''',
    tools=[get_user_transactions, categorize_user_transaction, create_user_goal]
)

goal_setting_agent = Agent(
    model='gemini-2.0-flash-001',
    name='goal_setting_agent',
    description='Helps users create and track SMART financial goals.',
    instruction='''
    You help users set and achieve financial goals by:
    1. Creating SMART savings and investment goals
    2. Breaking down large goals into actionable steps
    3. Tracking progress toward goals
    4. Providing motivation and adjustments
    Always make goals specific, measurable, and realistic.
    ''',
    tools=[create_user_goal, get_user_account_balances]
)

reporting_agent = Agent(
    model='gemini-2.0-flash-001',
    name='reporting_agent',
    description='Creates financial reports and visualizations.',
    instruction='''
    You create comprehensive financial reports including:
    1. Spending analysis and trends
    2. Income tracking and forecasting
    3. Net worth calculations
    4. Investment performance
    5. Budget vs actual comparisons
    Present data clearly with actionable insights.
    ''',
    tools=[generate_user_report, get_user_transactions, get_user_account_balances]
)

investment_agent = Agent(
    model='gemini-2.0-flash-001',
    name='investment_agent',
    description='Provides investment planning and portfolio management guidance.',
    instruction='''
    You help users with investment decisions by:
    1. Analyzing risk tolerance and investment goals
    2. Suggesting portfolio allocations
    3. Explaining investment options and strategies
    4. Monitoring portfolio performance
    Always emphasize diversification and long-term thinking.
    ''',
    tools=[get_user_account_balances, generate_user_report, google_search]
)

# Main Orchestrator Agent
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='finance_orchestrator',
    description='Main finance assistant that coordinates specialized agents.',
    instruction='''
    You are the main finance assistant that helps users with all aspects of personal finance.
    
    Based on user requests, you should:
    1. Understand the user's financial intent
    2. Route to appropriate specialized agents when needed
    3. Coordinate responses from multiple agents
    4. Provide comprehensive, personalized financial guidance
    
    Available specialized agents:
    - onboarding_agent: Account setup and initial configuration
    - cash_flow_agent: Transaction categorization and budgeting  
    - goal_setting_agent: Financial goal creation and tracking
    - reporting_agent: Financial reports and analysis
    - investment_agent: Investment planning and portfolio management
    
    Always be helpful, accurate, and focused on the user's financial wellbeing.
    ''',
    tools=[get_user_transactions, get_user_account_balances, generate_user_report, google_search],
    sub_agents=[
        onboarding_agent,
        cash_flow_agent, 
        goal_setting_agent,
        reporting_agent,
        investment_agent
    ]
)
