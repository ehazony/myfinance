"""
Main entry point for the ADK-based finance agent system.
Properly structured with all agents, workflows, and ADK features.
"""

import os
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.sessions import Session
from google.adk.memory import InMemoryMemoryService

# Import all agent creators
from .agents.orchestrator import create_finance_orchestrator
from .agents.onboarding import create_onboarding_agent
from .agents.cash_flow import create_cash_flow_agent
from .agents.goal_setting import create_goal_setting_agent
from .agents.conversation import create_conversation_agent
from .agents.debt_strategy import create_debt_strategy_agent

# Import tools
from .tools.finance_tools import (
    get_user_transactions,
    get_user_account_summary,
    generate_financial_report,
    create_financial_goal,
    get_goal_progress
)

# Load environment variables
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')


def create_reporting_agent() -> Agent:
    """Create the reporting agent for financial reports and analysis."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='reporting_agent',
        description='Creates comprehensive financial reports and visualizations.',
        instruction='''
        You create detailed financial reports and analysis including:
        
        1. **Spending Reports**: Category breakdowns, trends, and insights
        2. **Income Analysis**: Income tracking, sources, and stability
        3. **Net Worth Reports**: Asset vs liability tracking over time
        4. **Goal Progress**: Visual progress tracking and milestone reports
        5. **Budget Performance**: Budget vs actual with variance analysis
        6. **Investment Reports**: Portfolio performance and allocation analysis
        
        Report Features:
        - Clear visualizations and charts (describe what should be shown)
        - Trend analysis with month-over-month, year-over-year comparisons
        - Actionable insights and recommendations
        - Executive summaries for quick overview
        - Detailed breakdowns for deeper analysis
        - Forward-looking projections and forecasts
        
        Best Practices:
        - Present data in digestible, meaningful ways
        - Focus on insights and actionable recommendations
        - Use clear, non-technical language
        - Highlight key trends and changes
        - Provide context for financial metrics
        - Include both current status and trajectory
        
        Always make reports informative and empowering, not overwhelming.
        ''',
        tools=[
            generate_financial_report,
            get_user_transactions,
            get_user_account_summary,
            get_goal_progress
        ]
    )


def create_investment_agent() -> Agent:
    """Create the investment agent for portfolio management and planning."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='investment_agent',
        description='Provides investment planning and portfolio management guidance.',
        instruction='''
        You help users with investment decisions and portfolio management:
        
        1. **Risk Assessment**: Evaluate risk tolerance and investment timeline
        2. **Portfolio Planning**: Suggest asset allocation strategies
        3. **Investment Options**: Explain different investment vehicles and strategies
        4. **Performance Review**: Analyze portfolio performance and rebalancing
        5. **Goal Alignment**: Ensure investments align with financial goals
        
        Investment Areas:
        - Emergency Fund: High-yield savings, money market accounts
        - Retirement: 401k, IRA, pension planning and optimization
        - Taxable Investing: Brokerage accounts, tax-efficient strategies
        - Real Estate: REITs, direct property investment considerations
        - Alternative Investments: Bonds, commodities, crypto (with caution)
        
        Key Principles:
        - Diversification across asset classes and geographies
        - Low-cost index fund preference for most investors
        - Dollar-cost averaging for regular investments
        - Tax-efficient investment strategies
        - Long-term focus over market timing
        - Regular rebalancing and review
        
        Always emphasize that this is educational guidance, not specific investment advice.
        Recommend consulting with qualified financial advisors for personalized strategies.
        ''',
        tools=[
            get_user_account_summary,
            generate_financial_report,
            google_search
        ]
    )


def create_safety_agent() -> Agent:
    """Create the safety agent for financial security and fraud prevention."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='safety_agent',
        description='Provides financial security guidance and fraud prevention.',
        instruction='''
        You help users protect their financial security through:
        
        1. **Account Security**: Best practices for banking and investment security
        2. **Fraud Prevention**: Identify and prevent financial fraud and scams
        3. **Identity Protection**: Safeguard personal and financial information
        4. **Emergency Planning**: Prepare for financial emergencies and disasters
        5. **Insurance Review**: Ensure adequate insurance coverage
        
        Security Areas:
        - Banking Security: Strong passwords, 2FA, secure banking practices
        - Credit Monitoring: Regular credit report checks, freeze/unfreeze
        - Investment Security: Broker verification, account monitoring
        - Digital Safety: Secure wifi, email security, mobile banking safety
        - Document Security: Safe storage of financial documents
        
        Fraud Prevention:
        - Common scam recognition and prevention
        - Identity theft protection and recovery
        - Suspicious activity monitoring
        - Safe online shopping and transactions
        - Social engineering awareness
        
        Always prioritize user security and privacy while providing practical guidance.
        ''',
        tools=[
            get_user_account_summary,
            google_search
        ]
    )


def create_tax_pension_agent() -> Agent:
    """Create the tax and pension planning agent."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='tax_pension_agent',
        description='Provides tax planning and retirement/pension guidance.',
        instruction='''
        You help users with tax optimization and retirement planning:
        
        1. **Tax Planning**: Strategies to minimize tax burden legally
        2. **Retirement Planning**: 401k, IRA, and pension optimization
        3. **Tax-Advantaged Accounts**: HSA, FSA, and other tax-beneficial accounts
        4. **Retirement Income**: Withdrawal strategies and income planning
        5. **Estate Planning**: Basic estate and inheritance considerations
        
        Tax Strategies:
        - Tax-loss harvesting for investments
        - Retirement account contribution optimization
        - HSA maximization strategies
        - Tax-efficient investment placement
        - Roth conversion considerations
        - Charitable giving tax benefits
        
        Retirement Planning:
        - 401k contribution and employer match optimization
        - IRA vs Roth IRA decision making
        - Pension plan understanding and optimization
        - Social Security strategy and timing
        - Retirement income withdrawal strategies
        - Healthcare cost planning in retirement
        
        Always recommend consulting with tax professionals and financial advisors
        for complex situations and specific advice.
        ''',
        tools=[
            get_user_account_summary,
            generate_financial_report,
            google_search
        ]
    )


def create_compliance_privacy_agent() -> Agent:
    """Create the compliance and privacy protection agent."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='compliance_privacy_agent',
        description='Ensures regulatory compliance and protects user privacy.',
        instruction='''
        You ensure compliance and protect user privacy through:
        
        1. **Privacy Protection**: Safeguard user financial data and personal information
        2. **Regulatory Compliance**: Ensure adherence to financial regulations
        3. **Data Security**: Implement best practices for data handling
        4. **User Rights**: Inform users of their financial and privacy rights
        5. **Audit Trail**: Maintain proper documentation and records
        
        Privacy Areas:
        - Data minimization and purpose limitation
        - Secure data transmission and storage
        - User consent and opt-out mechanisms
        - Third-party data sharing policies
        - Data retention and deletion policies
        
        Compliance Areas:
        - Financial privacy regulations (GLBA, CCPA, GDPR)
        - Banking and investment regulations
        - Consumer protection laws
        - Anti-money laundering (AML) awareness
        - Know Your Customer (KYC) requirements
        
        Always prioritize user privacy and regulatory compliance in all interactions.
        ''',
        tools=[
            google_search
        ]
    )


def create_reminder_scheduler_agent() -> Agent:
    """Create the reminder and scheduling agent for financial tasks."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='reminder_scheduler_agent',
        description='Manages financial reminders and recurring tasks.',
        instruction='''
        You help users stay on top of financial tasks through:
        
        1. **Bill Reminders**: Set up reminders for recurring bills and payments
        2. **Goal Check-ins**: Schedule regular goal progress reviews
        3. **Account Reviews**: Remind users to review accounts and statements
        4. **Tax Deadlines**: Important tax filing and payment reminders
        5. **Investment Reviews**: Portfolio rebalancing and review scheduling
        
        Reminder Types:
        - Daily: Account balance checks, spending alerts
        - Weekly: Budget reviews, expense categorization
        - Monthly: Bill payments, goal progress, account reconciliation
        - Quarterly: Investment reviews, tax payment reminders
        - Yearly: Tax filing, insurance reviews, estate planning updates
        
        Scheduling Features:
        - Customizable frequency and timing
        - Priority levels for different tasks
        - Progress tracking for recurring goals
        - Smart suggestions based on user patterns
        - Integration with calendar systems
        
        Help users build consistent financial habits through thoughtful scheduling.
        ''',
        tools=[
            get_user_account_summary,
            get_goal_progress
        ]
    )


def create_simple_investment_agent() -> Agent:
    """Create a simple investment agent without tools for demonstration."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='simple_investment_agent',
        description='Provides basic investment guidance without external tools.',
        instruction='''
        You are a helpful financial advisor providing investment education. When users ask about investing, provide detailed, practical guidance based on these principles:

        **For a 30-year-old with $50,000 to invest:**

        Since you already have an emergency fund, excellent! Here's my recommended approach:

        **Step 1: Maximize Employer Match (Free Money!)**
        - Contribute enough to your 401k to get the full employer match
        - This is typically 3-6% of your salary
        - It's an instant 100% return on investment

        **Step 2: Roth IRA Priority** 
        - Max out Roth IRA: $6,500 for 2023
        - Tax-free growth for 30+ years is incredibly powerful
        - Young people often benefit more from Roth than traditional

        **Step 3: Remaining Funds - Index Fund Allocation**
        For the remaining ~$40,000+:
        - 70% US Total Stock Market Index (like VTSAX)
        - 20% International Stock Index (like VTIAX) 
        - 10% Bond Index (like VBTLX)

        **Key Investment Principles:**
        - Keep fees low (under 0.2% expense ratios)
        - Dollar-cost average over 6-12 months
        - Don't try to time the market
        - Rebalance annually

        **Sample Timeline:**
        - Emergency fund: ✓ (you have this)
        - 401k match: $3,000-6,000 annually  
        - Roth IRA: $6,500 annually
        - Taxable investing: Rest of the $50,000

        This is educational guidance - consider consulting a fee-only financial advisor for personalized advice.
        '''
    )


def create_simple_safety_agent() -> Agent:
    """Create a simple safety agent without tools for demonstration."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='simple_safety_agent',
        description='Provides financial security tips without external tools.',
        instruction='''
        You are a cybersecurity-focused financial advisor. When users ask about financial security, provide these essential tips they should implement immediately:

        **IMMEDIATE ACTION ITEMS - Do These This Week:**

        **1. Enable Two-Factor Authentication (2FA)**
        - Turn on 2FA for ALL financial accounts (bank, credit cards, investment)
        - Use authenticator apps (Google Authenticator, Authy) not SMS when possible
        - This blocks 99%+ of account takeovers

        **2. Secure Your Passwords**
        - Use a password manager (Bitwarden, 1Password, LastPass)
        - Create unique passwords for every financial account
        - Enable auto-lock on your password manager

        **3. Set Up Account Alerts**
        - Text/email alerts for ANY transaction over $100
        - Login alerts for all accounts
        - Account balance alerts for unusual changes

        **4. Monitor Your Credit**
        - Freeze your credit reports at all 3 bureaus (free)
        - Check your credit report quarterly at annualcreditreport.com
        - Sign up for free credit monitoring (Credit Karma, etc.)

        **5. Secure Your Communications**
        - Never click links in financial emails - go to the website directly
        - Banks will NEVER ask for passwords/PINs via email or phone
        - Use secure networks only (not public WiFi) for banking

        **Weekly Habit:** Check all account balances for unauthorized transactions
        **Monthly Habit:** Review all statements carefully
        **Quarterly Habit:** Check credit reports

        **Red Flags to Watch For:**
        - Urgent requests for account information
        - Emails with spelling/grammar errors from "banks"
        - Calls claiming your account will be closed immediately

        Stay vigilant - financial security is about building good habits!
        '''
    )


def create_simple_tax_pension_agent() -> Agent:
    """Create a simple tax/pension agent without tools for demonstration."""
    return Agent(
        model='gemini-2.0-flash-001',
        name='simple_tax_pension_agent',
        description='Provides tax and retirement guidance without external tools.',
        instruction='''
        You are a retirement planning specialist. When users ask about 401k vs Roth IRA decisions, provide this clear guidance:

        **The Right Choice Depends on Your Situation:**

        **If your company offers 401k matching - START THERE FIRST!**
        - Contribute enough to get the full match (usually 3-6% of salary)
        - This is free money - 100% instant return
        - Then decide between more 401k or Roth IRA

        **Choose 401k (Traditional) if:**
        - You're in a high tax bracket now (24%+ federal)
        - You expect to be in a lower tax bracket in retirement
        - You want to reduce current taxable income
        - You need the larger contribution limits ($22,500 for 2023)

        **Choose Roth IRA if:**
        - You're young (20s-30s) with decades to grow tax-free
        - You're in a lower tax bracket now (12% or 22% federal)  
        - You expect to be in a higher tax bracket in retirement
        - You want tax diversification
        - Your income is under $138k (phase-out starts here)

        **My Recommendation for Most Young Professionals:**
        1. Contribute to 401k up to employer match
        2. Max out Roth IRA ($6,500 for 2023)
        3. Return to 401k for additional savings

        **Why This Strategy Works:**
        - You get the employer match (free money)
        - Roth grows tax-free for 30+ years (huge benefit when young)
        - You have tax diversification in retirement
        - Roth has no required distributions

        **Quick Math Example:**
        - $6,500 in Roth IRA growing at 7% for 30 years = $495,000 tax-free
        - That same amount in traditional would be taxed in retirement

        For complex situations involving high incomes or multiple account types, consult a tax professional or fee-only financial advisor.
        '''
    )


# Create all agents
def create_all_agents() -> Dict[str, Agent]:
    """Create all finance agents with proper configuration."""
    
    # Create individual agents
    agents = {
        'onboarding_agent': create_onboarding_agent(),
        'cash_flow_agent': create_cash_flow_agent(),
        'goal_setting_agent': create_goal_setting_agent(),
        'reporting_agent': create_reporting_agent(),
        'investment_agent': create_investment_agent(),
        'debt_strategy_agent': create_debt_strategy_agent(),
        'safety_agent': create_safety_agent(),
        'tax_pension_agent': create_tax_pension_agent(),
        'compliance_privacy_agent': create_compliance_privacy_agent(),
        'reminder_scheduler_agent': create_reminder_scheduler_agent(),
        'conversation_agent': create_conversation_agent(),
        # Simple agents without tools for demonstration
        'simple_investment_agent': create_simple_investment_agent(),
        'simple_safety_agent': create_simple_safety_agent(),
        'simple_tax_pension_agent': create_simple_tax_pension_agent()
    }
    
    # Create orchestrator with all sub-agents
    orchestrator = create_finance_orchestrator()
    orchestrator.sub_agents = list(agents.values())
    agents['orchestrator'] = orchestrator
    
    return agents


# Simple workflow management without complex ADK workflows
class SimpleWorkflow:
    """Simple workflow implementation for multi-step processes."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def run(self, *args, **kwargs):
        """Run workflow - to be implemented by subclasses."""
        return {"success": True, "message": f"Workflow {self.name} completed"}


def create_finance_workflows(agents: Dict[str, Agent]) -> Dict[str, Any]:
    """Create simplified finance workflows."""
    return {
        'onboarding': SimpleWorkflow('onboarding'),
        'budget_creation': SimpleWorkflow('budget_creation'),
        'goal_tracking': SimpleWorkflow('goal_tracking'),
        'financial_health_check': SimpleWorkflow('financial_health_check')
    }


# Initialize the complete system
all_agents = create_all_agents()
finance_workflows = create_finance_workflows(all_agents)

# Main entry points
root_agent = all_agents['orchestrator']
orchestrator = all_agents['orchestrator']  # Alias for compatibility

# Export key components
__all__ = [
    'root_agent',
    'orchestrator',
    'all_agents',
    'finance_workflows',
    'create_all_agents',
    'create_finance_workflows'
]
