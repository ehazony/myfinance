"""
Finance-specific tools for ADK agents.
Now implemented as wrappers around auto-generated OpenAPI client.

All tools use the ToolContext to access user session and authentication information.
The user token is retrieved from tool_context.state where it's stored by the agent service.
"""

import json
import sys
import os
from typing import Optional
import logging
from datetime import datetime
import calendar
from google.adk.tools.tool_context import ToolContext

# Add the parent directory to sys.path to allow absolute imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from tools.finance_data_client import get_finance_client

logger = logging.getLogger(__name__)

def get_user_transactions(tool_context: ToolContext, date_range: Optional[str] = None, category: Optional[str] = None, limit: Optional[int] = 100) -> str:
    """Get user transactions with filtering options. User is determined from authentication context via ToolContext.
    Both date_range and category are optional. If neither is provided, returns most recent transactions.
    
    Args:
        tool_context: ADK tool context with user session state
        date_range: Optional date range filter (e.g., "2024-01" or "2024-01-01:2024-01-31")
        category: Optional category filter
        limit: Maximum number of transactions to return (default: 100)
    """
    logger.info(f"Entering get_user_transactions: date_range='{date_range}', category='{category}', limit={limit}")
    
    if limit is None or limit <= 0:
        logger.info(f"Limit was {limit}, resetting to default 100.")
        limit = 100
        
    try:
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            logger.error("No authentication token available in session.")
            return json.dumps({'error': 'No authentication token available in session'})
        logger.info("Successfully retrieved authentication token.")

        client = get_finance_client()
        
        start_date_str = None
        end_date_str = None

        if date_range:
            logger.info(f"Processing date_range: '{date_range}'")
            try:
                if ':' in date_range:  # Format "YYYY-MM-DD:YYYY-MM-DD"
                    s_date, e_date = date_range.split(':', 1)
                    # Basic validation for date format
                    datetime.strptime(s_date, '%Y-%m-%d')
                    datetime.strptime(e_date, '%Y-%m-%d')
                    start_date_str = s_date
                    end_date_str = e_date
                    logger.info(f"Parsed date range: start='{start_date_str}', end='{end_date_str}'")
                elif len(date_range) == 7 and date_range[4] == '-':  # Format "YYYY-MM"
                    year_str, month_str = date_range.split('-', 1)
                    year = int(year_str)
                    month = int(month_str)
                    if not (1 <= month <= 12):
                        raise ValueError("Month out of valid range (1-12)")
                    
                    start_date_dt = datetime(year, month, 1)
                    start_date_str = start_date_dt.strftime('%Y-%m-%d')
                    
                    _, last_day = calendar.monthrange(year, month)
                    end_date_dt = datetime(year, month, last_day)
                    end_date_str = end_date_dt.strftime('%Y-%m-%d')
                    logger.info(f"Parsed month range: start='{start_date_str}', end='{end_date_str}'")
                else:
                    logger.warning(f"Invalid date_range format: '{date_range}'. Expected 'YYYY-MM' or 'YYYY-MM-DD:YYYY-MM-DD'. No date filter will be applied.")
            except ValueError as ve:
                logger.warning(f"Error parsing date_range '{date_range}': {ve}. No date filter will be applied.")
                start_date_str = None # Ensure reset on error
                end_date_str = None
        else:
            logger.info("No date_range provided. No date filtering will be applied.")

        logger.info(f"Calling finance client get_filtered_transactions_sync with: token=HIDDEN, category='{category}', start_date='{start_date_str}', end_date='{end_date_str}', limit={limit}")
        
        transactions = client.get_filtered_transactions_sync(
            token=token,
            category=category,
            start_date=start_date_str, # Use the parsed strings
            end_date=end_date_str,   # Use the parsed strings
            limit=limit
        )
        logger.info(f"Received {len(transactions)} transactions from client.")
        logger.debug(f"Raw transactions response (first 2 if many): {transactions[:2]}")

        return json.dumps({
            'transactions': transactions,
            'filters': {
                'original_date_range': date_range, # Keep original for reference
                'parsed_start_date': start_date_str,
                'parsed_end_date': end_date_str,
                'category': category,
                'limit': limit
            }
        })
    except Exception as e:
        logger.error(f"Error in get_user_transactions: {str(e)}", exc_info=True)
        return json.dumps({'error': f'Failed to get transactions: {str(e)}'})


def get_user_account_summary(tool_context: ToolContext) -> str:
    """Get comprehensive account summary for user. User is determined from authentication context via ToolContext."""
    try:
        # Get user token from session state
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            return json.dumps({'error': 'No authentication token available in session'})
        
        client = get_finance_client()
        accounts = client.get_account_summary_sync(token=token)
        return json.dumps({
            'accounts': accounts
        })
    except Exception as e:
        return json.dumps({'error': f'Failed to get account summary: {str(e)}'})


def categorize_transaction(tool_context: ToolContext, transaction_id: str, category: str) -> str:
    """Stub: Not implemented in OpenAPI tools yet. User is determined from authentication context via ToolContext."""
    return json.dumps({'error': 'categorize_transaction is not implemented in OpenAPI tools.'})


def get_spending_analysis(tool_context: ToolContext, period: str = "month") -> str:
    """Stub: Not implemented in OpenAPI tools yet. User is determined from authentication context via ToolContext."""
    if not period:
        period = "month"
    return json.dumps({'error': 'get_spending_analysis is not implemented in OpenAPI tools.'})


def generate_financial_report(tool_context: ToolContext, report_type: str, period: str = "month") -> str:
    """Generate comprehensive financial reports. User is determined from authentication context via ToolContext."""
    if not period:
        period = "month"
    try:
        # Get user token from session state
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            return json.dumps({'error': 'No authentication token available in session'})
        
        client = get_finance_client()
        if report_type == "budget_analysis":
            data = client.get_budget_analysis_sync(token=token, period=period)
            return json.dumps({
                'report_type': report_type,
                'period': period,
                'data': data
            })
        elif report_type == "spending_analysis":
            transactions = client.get_filtered_transactions_sync(token=token, limit=500)
            return json.dumps({
                'report_type': report_type,
                'period': period,
                'transactions': transactions
            })
        elif report_type == "financial_context":
            context_data = client.get_financial_context_sync(token=token)
            return json.dumps({
                'report_type': report_type,
                'context': context_data
            })
        else:
            return json.dumps({
                'error': f'Unknown report type: {report_type}. Available: budget_analysis, spending_analysis, financial_context'
            })
    except Exception as e:
        return json.dumps({'error': f'Failed to generate report: {str(e)}'})


def create_financial_goal(tool_context: ToolContext, goal_name: str, target_amount: float, goal_type: str = "savings", category: Optional[str] = None, deadline: Optional[str] = None) -> str:
    """Create a financial goal (placeholder - not implemented in OpenAPI yet). User is determined from authentication context via ToolContext."""
    if not goal_type:
        goal_type = "savings"
    return json.dumps({
        'error': 'create_financial_goal endpoint not yet implemented in OpenAPI specification',
        'requested_goal': {
            'name': goal_name,
            'target_amount': target_amount,
            'category': category,
            'deadline': deadline,
            'type': goal_type
        }
    })


def get_goal_progress(tool_context: ToolContext) -> str:
    """Get progress on financial goals (placeholder - not implemented in OpenAPI yet). User is determined from authentication context via ToolContext."""
    return json.dumps({
        'error': 'get_goal_progress endpoint not yet implemented in OpenAPI specification',
        'suggestion': 'Use generate_financial_report with "financial_context" to get goal information'
    })


# Additional helper functions using the generated client

def get_user_budget_analysis(tool_context: ToolContext, period: str = "current_month") -> str:
    """Get budget vs actual spending analysis. User is determined from authentication context via ToolContext."""
    if not period:
        period = "current_month"
    try:
        # Get user token from session state
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            return json.dumps({'error': 'No authentication token available in session'})
        
        client = get_finance_client()
        analysis = client.get_budget_analysis_sync(token=token, period=period)
        return json.dumps({
            'period': period,
            'budget_analysis': analysis
        })
    except Exception as e:
        return json.dumps({'error': f'Failed to get budget analysis: {str(e)}'})


def get_conversation_context(tool_context: ToolContext) -> str:
    """Get conversation context for agent memory. User is determined from authentication context via ToolContext."""
    try:
        # Get user token from session state
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            return json.dumps({'error': 'No authentication token available in session'})
        
        client = get_finance_client()
        context_data = client.get_conversation_context_sync(token=token)
        return json.dumps({
            'context': context_data
        })
    except Exception as e:
        return json.dumps({'error': f'Failed to get conversation context: {str(e)}'})


def get_complete_financial_context(tool_context: ToolContext, limit_transactions: int = 100) -> str:
    """Get complete financial context for comprehensive agent analysis. User is determined from authentication context via ToolContext."""
    if limit_transactions is None or limit_transactions <= 0:
        limit_transactions = 100
    try:
        # Get user token from session state
        token = tool_context.state.get('user_token') or tool_context.state.get('token')
        if not token:
            return json.dumps({'error': 'No authentication token available in session'})
        
        client = get_finance_client()
        context_data = client.get_financial_context_sync(
            token=token,
            include_future_goals=True,
            limit_transactions=limit_transactions
        )
        return json.dumps({
            'financial_context': context_data
        })
    except Exception as e:
        return json.dumps({'error': f'Failed to get financial context: {str(e)}'}) 