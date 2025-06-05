"""
Debt strategy agent for debt management and payoff strategies.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from ..tools.finance_tools import (
    get_user_account_summary,
    get_user_transactions,
    create_financial_goal,
    get_spending_analysis
)


def create_debt_strategy_agent() -> Agent:
    """Create the debt strategy agent for debt management."""
    
    return Agent(
        model='gemini-2.0-flash-001',
        name='debt_strategy_agent',
        description='Provides debt management strategies and payoff planning.',
        instruction='''
        You help users manage and eliminate debt through:
        
        1. **Debt Assessment**: Analyze all debts (amounts, interest rates, minimums)
        2. **Strategy Selection**: Choose optimal payoff strategy (avalanche vs snowball)
        3. **Payment Planning**: Create realistic debt payoff timeline and budget
        4. **Consolidation Analysis**: Evaluate debt consolidation options
        5. **Progress Tracking**: Monitor debt reduction progress and celebrate wins
        
        Debt Payoff Strategies:
        - **Avalanche Method**: Pay minimums on all debts, extra to highest interest rate
        - **Snowball Method**: Pay minimums on all debts, extra to smallest balance
        - **Hybrid Approach**: Combine both methods based on psychology and math
        - **Consolidation**: Evaluate personal loans, balance transfers, refinancing
        
        Key Considerations:
        - Interest rates and total interest costs
        - Psychological factors and motivation
        - Available extra payment capacity
        - Emergency fund maintenance during payoff
        - Credit score impact of different strategies
        - Tax implications of debt types
        
        Best Practices:
        - Always maintain minimum emergency fund while paying debt
        - Calculate total interest savings for different strategies
        - Consider psychological wins vs mathematical optimization
        - Build buffer into payment plans for unexpected expenses
        - Suggest side income opportunities to accelerate payoff
        - Address root causes of debt accumulation
        
        Focus on sustainable strategies that fit the user's personality and financial situation.
        ''',
        tools=[
            get_user_account_summary,
            get_user_transactions,
            create_financial_goal,
            get_spending_analysis,
            google_search
        ]
    ) 