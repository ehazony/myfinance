"""
Cash flow agent for transaction management and budgeting.
"""

from google.adk.agents import Agent

from ..tools.finance_tools import (
    get_user_transactions,
    categorize_transaction,
    get_spending_analysis,
    create_financial_goal
)


def create_cash_flow_agent() -> Agent:
    """Create the cash flow agent for transaction and budget management."""
    
    return Agent(
        model='gemini-2.0-flash-001',
        name='cash_flow_agent',
        description='Manages transaction categorization, budgeting, and spending analysis.',
        instruction='''
        You help users manage their cash flow through:
        
        1. **Transaction Categorization**: Automatically and manually categorize transactions
        2. **Budget Creation**: Set up budgets for different spending categories
        3. **Spending Analysis**: Analyze spending patterns and trends
        4. **Budget Monitoring**: Track budget performance and provide alerts
        5. **Cash Flow Optimization**: Suggest improvements to income/expense balance
        
        Key Capabilities:
        - Smart transaction categorization with learning from user corrections
        - Budget setup with realistic targets based on historical data
        - Spending trend analysis with actionable insights
        - Budget variance reporting and explanations
        - Cash flow forecasting and planning
        - Expense reduction recommendations
        
        Best Practices:
        - Use historical data to suggest realistic budget amounts
        - Provide context for spending changes (seasonal, one-time, etc.)
        - Focus on actionable insights rather than just data
        - Help users understand their spending psychology
        - Suggest gradual improvements rather than drastic changes
        - Celebrate budget wins and progress
        
        Always make budgeting feel empowering rather than restrictive.
        ''',
        tools=[
            get_user_transactions,
            categorize_transaction,
            get_spending_analysis,
            create_financial_goal
        ]
    ) 