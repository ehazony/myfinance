"""
Django integration module for ADK agents.
Provides tools that interface with the existing Django models and database.
"""

import os
import sys
import django
from pathlib import Path

# Add the parent directory to Python path to import Django models
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
django.setup()

# Now we can import Django models (using correct models from the codebase)
from myFinance.models import Transaction, Credential, Tag, TagGoal
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json


def get_user_transactions(user_id: str, date_range: str = None, category: str = None) -> str:
    """Get user transactions from the database.
    
    Args:
        user_id: The user identifier
        date_range: Optional date range filter (e.g., "2024-01" or "2024-01-01:2024-01-31")
        category: Optional category filter
        
    Returns:
        JSON string of transaction data
    """
    try:
        user = User.objects.get(id=user_id)
        transactions = Transaction.objects.filter(user=user)
        
        # Apply date range filter
        if date_range:
            if ':' in date_range:
                start_date, end_date = date_range.split(':')
                transactions = transactions.filter(
                    date__gte=datetime.fromisoformat(start_date),
                    date__lte=datetime.fromisoformat(end_date)
                )
            else:
                # Assume month format like "2024-01"
                year, month = date_range.split('-')
                transactions = transactions.filter(
                    date__year=int(year),
                    date__month=int(month)
                )
        
        # Apply category filter
        if category:
            transactions = transactions.filter(tag__name__icontains=category)
        
        # Convert to JSON-serializable format
        data = []
        for tx in transactions[:100]:  # Limit to 100 for performance
            data.append({
                'id': tx.id,
                'date': tx.date.isoformat(),
                'amount': float(tx.value),  # Note: using 'value' field from model
                'description': tx.name,     # Note: using 'name' field from model
                'category': tx.tag.name if tx.tag else 'Uncategorized',
                'credential': tx.credential.company if tx.credential else 'Unknown'
            })
        
        return json.dumps({
            'transactions': data,
            'total_count': transactions.count(),
            'showing': len(data)
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get transactions: {str(e)}'})


def get_user_account_balances(user_id: str, account_type: str = None) -> str:
    """Get user account balances.
    
    Args:
        user_id: The user identifier
        account_type: Optional account type filter
        
    Returns:
        JSON string of account balance data
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Calculate balances from transactions
        income = Transaction.objects.filter(
            user=user, 
            value__gt=0
        ).aggregate(total=Sum('value'))['total'] or 0
        
        expenses = Transaction.objects.filter(
            user=user, 
            value__lt=0
        ).aggregate(total=Sum('value'))['total'] or 0
        
        net_worth = income + expenses  # expenses are negative
        
        # Get recent transactions for trend
        last_month = timezone.now() - timedelta(days=30)
        recent_expenses = Transaction.objects.filter(
            user=user,
            value__lt=0,
            date__gte=last_month
        ).aggregate(total=Sum('value'))['total'] or 0
        
        # Get credentials info
        credentials = []
        for cred in Credential.objects.filter(user=user):
            credentials.append({
                'company': cred.company,
                'type': cred.type,
                'balance': cred.balance,
                'last_scanned': cred.last_scanned.isoformat() if cred.last_scanned else None
            })
        
        return json.dumps({
            'user_id': user_id,
            'total_income': float(income),
            'total_expenses': float(abs(expenses)),
            'net_worth': float(net_worth),
            'monthly_spending': float(abs(recent_expenses)),
            'credentials': credentials,
            'last_updated': timezone.now().isoformat()
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get account balance: {str(e)}'})


def categorize_user_transaction(user_id: str, transaction_id: str, category: str) -> str:
    """Categorize a transaction.
    
    Args:
        user_id: The user identifier  
        transaction_id: The transaction identifier
        category: The category to assign
        
    Returns:
        Success message
    """
    try:
        user = User.objects.get(id=user_id)
        transaction = Transaction.objects.get(id=transaction_id, user=user)
        
        # Get or create tag
        tag, created = Tag.objects.get_or_create(
            name=category,
            user=user,
            defaults={'expense': transaction.value < 0}  # Set expense flag based on transaction
        )
        
        transaction.tag = tag
        transaction.save()
        
        return json.dumps({
            'success': True,
            'message': f'Transaction {transaction_id} categorized as {category}',
            'transaction': {
                'id': transaction.id,
                'description': transaction.name,
                'amount': float(transaction.value),
                'category': category
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to categorize transaction: {str(e)}'})


def create_user_goal(user_id: str, goal_name: str, target_amount: float, 
                    category: str = None, deadline: str = None) -> str:
    """Create a financial goal using TagGoal.
    
    Args:
        user_id: The user identifier
        goal_name: Name of the goal
        target_amount: Target amount for the goal
        category: Optional category for the goal
        deadline: Optional deadline (ISO format)
        
    Returns:
        Success message with goal ID
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Create or get the tag for this goal
        if category:
            tag, created = Tag.objects.get_or_create(
                name=category,
                user=user,
                defaults={'expense': False}  # Goals are typically income/savings targets
            )
        else:
            tag, created = Tag.objects.get_or_create(
                name=goal_name,
                user=user,
                defaults={'expense': False}
            )
        
        # Create TagGoal
        tag_goal, created = TagGoal.objects.get_or_create(
            user=user,
            tag=tag,
            defaults={'value': target_amount}
        )
        
        if not created:
            tag_goal.value = target_amount
            tag_goal.save()
        
        return json.dumps({
            'success': True,
            'message': f'Goal "{goal_name}" created successfully',
            'goal': {
                'id': tag_goal.id,
                'name': goal_name,
                'target_amount': target_amount,
                'category': tag.name,
                'tag_id': tag.id
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to create goal: {str(e)}'})


def generate_user_report(user_id: str, report_type: str, period: str = "month") -> str:
    """Generate financial reports.
    
    Args:
        user_id: The user identifier
        report_type: Type of report (spending, income, net_worth, categories)
        period: Report period (week, month, quarter, year)
        
    Returns:
        Report data as JSON string
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Calculate date range based on period
        end_date = timezone.now()
        if period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        elif period == "quarter":
            start_date = end_date - timedelta(days=90)
        elif period == "year":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)  # Default to month
        
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        if report_type == "spending":
            spending_by_category = {}
            for tx in transactions.filter(value__lt=0):
                category = tx.tag.name if tx.tag else 'Uncategorized'
                spending_by_category[category] = spending_by_category.get(category, 0) + abs(float(tx.value))
            
            return json.dumps({
                'report_type': 'spending',
                'period': period,
                'spending_by_category': spending_by_category,
                'total_spending': sum(spending_by_category.values()),
                'date_range': f"{start_date.date()} to {end_date.date()}"
            })
        
        elif report_type == "income":
            total_income = transactions.filter(value__gt=0).aggregate(
                total=Sum('value')
            )['total'] or 0
            
            return json.dumps({
                'report_type': 'income',
                'period': period,
                'total_income': float(total_income),
                'date_range': f"{start_date.date()} to {end_date.date()}"
            })
        
        elif report_type == "net_worth":
            income = transactions.filter(value__gt=0).aggregate(total=Sum('value'))['total'] or 0
            expenses = transactions.filter(value__lt=0).aggregate(total=Sum('value'))['total'] or 0
            
            return json.dumps({
                'report_type': 'net_worth',
                'period': period,
                'income': float(income),
                'expenses': float(abs(expenses)),
                'net_change': float(income + expenses),
                'date_range': f"{start_date.date()} to {end_date.date()}"
            })
        
        else:
            return json.dumps({'error': f'Unknown report type: {report_type}'})
            
    except Exception as e:
        return json.dumps({'error': f'Failed to generate report: {str(e)}'})


# Export the integration functions
__all__ = [
    'get_user_transactions',
    'get_user_account_balances', 
    'categorize_user_transaction',
    'create_user_goal',
    'generate_user_report'
] 