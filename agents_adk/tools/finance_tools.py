"""
Finance-specific tools for ADK agents.
Integrates with Django models and provides finance domain functionality.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Django setup
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')

import django
django.setup()

from myFinance.models import Transaction, Credential, Tag, TagGoal
from django.contrib.auth.models import User
from django.db.models import Sum, Q, Avg
from django.utils import timezone


def get_user_transactions(user_id: str, date_range: Optional[str] = None, 
                         category: Optional[str] = None, limit: int = 100) -> str:
    """Get user transactions with filtering options.
    
    Args:
        user_id: The user identifier
        date_range: Date range filter (e.g., "2024-01" or "2024-01-01:2024-01-31")
        category: Category filter
        limit: Maximum number of transactions to return
        
    Returns:
        JSON string of transaction data with metadata
    """
    try:
        user = User.objects.get(id=user_id)
        transactions = Transaction.objects.filter(user=user).order_by('-date')
        
        # Apply date range filter
        if date_range:
            if ':' in date_range:
                start_date, end_date = date_range.split(':')
                transactions = transactions.filter(
                    date__gte=datetime.fromisoformat(start_date),
                    date__lte=datetime.fromisoformat(end_date)
                )
            else:
                # Month format
                year, month = date_range.split('-')
                transactions = transactions.filter(
                    date__year=int(year),
                    date__month=int(month)
                )
        
        # Apply category filter
        if category:
            transactions = transactions.filter(
                Q(tag__name__icontains=category) | 
                Q(name__icontains=category)
            )
        
        # Get transactions with limit
        transaction_list = transactions[:limit]
        
        # Calculate summary statistics
        total_income = transactions.filter(value__gt=0).aggregate(Sum('value'))['value__sum'] or 0
        total_expenses = transactions.filter(value__lt=0).aggregate(Sum('value'))['value__sum'] or 0
        
        # Convert to JSON-serializable format
        data = []
        for tx in transaction_list:
            data.append({
                'id': tx.id,
                'date': tx.date.isoformat(),
                'amount': float(tx.value),
                'description': tx.name,
                'category': tx.tag.name if tx.tag else 'Uncategorized',
                'account': tx.credential.company if tx.credential else 'Unknown',
                'is_income': tx.value > 0
            })
        
        return json.dumps({
            'transactions': data,
            'summary': {
                'total_count': transactions.count(),
                'showing': len(data),
                'total_income': float(total_income),
                'total_expenses': float(abs(total_expenses)),
                'net_flow': float(total_income + total_expenses)
            },
            'filters': {
                'date_range': date_range,
                'category': category,
                'limit': limit
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get transactions: {str(e)}'})


def get_user_account_summary(user_id: str) -> str:
    """Get comprehensive account summary for user.
    
    Args:
        user_id: The user identifier
        
    Returns:
        JSON string with complete financial overview
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Get all credentials/accounts
        credentials = Credential.objects.filter(user=user)
        
        # Calculate balances from transactions
        all_transactions = Transaction.objects.filter(user=user)
        income = all_transactions.filter(value__gt=0).aggregate(Sum('value'))['value__sum'] or 0
        expenses = all_transactions.filter(value__lt=0).aggregate(Sum('value'))['value__sum'] or 0
        
        # Recent activity (last 30 days)
        last_month = timezone.now() - timedelta(days=30)
        recent_income = all_transactions.filter(
            value__gt=0, date__gte=last_month
        ).aggregate(Sum('value'))['value__sum'] or 0
        recent_expenses = all_transactions.filter(
            value__lt=0, date__gte=last_month
        ).aggregate(Sum('value'))['value__sum'] or 0
        
        # Account details
        account_details = []
        for cred in credentials:
            account_transactions = all_transactions.filter(credential=cred)
            account_balance = account_transactions.aggregate(Sum('value'))['value__sum'] or 0
            
            account_details.append({
                'company': cred.company,
                'type': cred.type,
                'current_balance': cred.balance,
                'calculated_balance': float(account_balance),
                'last_scanned': cred.last_scanned.isoformat() if cred.last_scanned else None,
                'transaction_count': account_transactions.count()
            })
        
        return json.dumps({
            'user_id': user_id,
            'overview': {
                'total_income': float(income),
                'total_expenses': float(abs(expenses)),
                'net_worth': float(income + expenses),
                'account_count': credentials.count()
            },
            'recent_activity': {
                'monthly_income': float(recent_income),
                'monthly_expenses': float(abs(recent_expenses)),
                'monthly_net': float(recent_income + recent_expenses)
            },
            'accounts': account_details,
            'last_updated': timezone.now().isoformat()
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get account summary: {str(e)}'})


def categorize_transaction(user_id: str, transaction_id: str, category: str) -> str:
    """Categorize a specific transaction.
    
    Args:
        user_id: The user identifier
        transaction_id: The transaction identifier
        category: The category to assign
        
    Returns:
        JSON confirmation of categorization
    """
    try:
        user = User.objects.get(id=user_id)
        transaction = Transaction.objects.get(id=transaction_id, user=user)
        
        # Get or create tag
        tag, created = Tag.objects.get_or_create(
            name=category,
            user=user,
            defaults={'expense': transaction.value < 0}
        )
        
        old_category = transaction.tag.name if transaction.tag else 'Uncategorized'
        transaction.tag = tag
        transaction.save()
        
        return json.dumps({
            'success': True,
            'transaction': {
                'id': transaction.id,
                'description': transaction.name,
                'amount': float(transaction.value),
                'date': transaction.date.isoformat(),
                'old_category': old_category,
                'new_category': category
            },
            'tag_info': {
                'tag_id': tag.id,
                'tag_created': created
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to categorize transaction: {str(e)}'})


def get_spending_analysis(user_id: str, period: str = "month") -> str:
    """Get detailed spending analysis by category.
    
    Args:
        user_id: The user identifier
        period: Analysis period (week, month, quarter, year)
        
    Returns:
        JSON string with spending breakdown and insights
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Calculate date range
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
            start_date = end_date - timedelta(days=30)
        
        # Get transactions for period
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date,
            value__lt=0  # Only expenses
        )
        
        # Group by category
        spending_by_category = {}
        transaction_count_by_category = {}
        
        for tx in transactions:
            category = tx.tag.name if tx.tag else 'Uncategorized'
            amount = abs(float(tx.value))
            
            spending_by_category[category] = spending_by_category.get(category, 0) + amount
            transaction_count_by_category[category] = transaction_count_by_category.get(category, 0) + 1
        
        # Calculate insights
        total_spending = sum(spending_by_category.values())
        avg_transaction = total_spending / len(transactions) if transactions else 0
        
        # Sort categories by spending
        sorted_categories = sorted(
            spending_by_category.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return json.dumps({
            'period': period,
            'date_range': f"{start_date.date()} to {end_date.date()}",
            'total_spending': total_spending,
            'transaction_count': transactions.count(),
            'average_transaction': avg_transaction,
            'spending_by_category': dict(sorted_categories),
            'transaction_count_by_category': transaction_count_by_category,
            'top_categories': sorted_categories[:5],
            'insights': {
                'largest_category': sorted_categories[0] if sorted_categories else None,
                'categories_count': len(spending_by_category),
                'daily_average': total_spending / 30 if period == "month" else None
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get spending analysis: {str(e)}'})


def create_financial_goal(user_id: str, goal_name: str, target_amount: float,
                         category: Optional[str] = None, deadline: Optional[str] = None,
                         goal_type: str = "savings") -> str:
    """Create a financial goal with progress tracking.
    
    Args:
        user_id: The user identifier
        goal_name: Name/description of the goal
        target_amount: Target amount to achieve
        category: Associated category for tracking
        deadline: Optional deadline (ISO format)
        goal_type: Type of goal (savings, expense_reduction, income)
        
    Returns:
        JSON confirmation with goal details
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Create or get tag for goal tracking
        tag_name = category or goal_name
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            user=user,
            defaults={'expense': goal_type == "expense_reduction"}
        )
        
        # Create or update TagGoal
        tag_goal, goal_created = TagGoal.objects.get_or_create(
            user=user,
            tag=tag,
            defaults={'value': target_amount}
        )
        
        if not goal_created:
            # Update existing goal
            tag_goal.value = target_amount
            tag_goal.save()
        
        # Calculate current progress
        if goal_type == "savings":
            current_amount = Transaction.objects.filter(
                user=user, tag=tag, value__gt=0
            ).aggregate(Sum('value'))['value__sum'] or 0
        elif goal_type == "expense_reduction":
            current_amount = abs(Transaction.objects.filter(
                user=user, tag=tag, value__lt=0
            ).aggregate(Sum('value'))['value__sum'] or 0)
        else:
            current_amount = Transaction.objects.filter(
                user=user, tag=tag
            ).aggregate(Sum('value'))['value__sum'] or 0
        
        progress_percentage = (current_amount / target_amount * 100) if target_amount > 0 else 0
        
        return json.dumps({
            'success': True,
            'goal': {
                'id': tag_goal.id,
                'name': goal_name,
                'target_amount': target_amount,
                'current_amount': float(current_amount),
                'progress_percentage': min(progress_percentage, 100),
                'category': tag.name,
                'type': goal_type,
                'deadline': deadline,
                'created': goal_created
            },
            'tag_info': {
                'tag_id': tag.id,
                'tag_created': created
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to create goal: {str(e)}'})


def get_goal_progress(user_id: str) -> str:
    """Get progress on all user financial goals.
    
    Args:
        user_id: The user identifier
        
    Returns:
        JSON with all goals and their progress
    """
    try:
        user = User.objects.get(id=user_id)
        goals = TagGoal.objects.filter(user=user)
        
        goal_progress = []
        for goal in goals:
            # Calculate current progress based on transactions
            tag_transactions = Transaction.objects.filter(user=user, tag=goal.tag)
            
            # Assume positive goals (savings) - could be enhanced based on goal type
            current_amount = tag_transactions.filter(value__gt=0).aggregate(
                Sum('value')
            )['value__sum'] or 0
            
            progress_percentage = (current_amount / goal.value * 100) if goal.value > 0 else 0
            
            goal_progress.append({
                'goal_id': goal.id,
                'category': goal.tag.name,
                'target_amount': float(goal.value),
                'current_amount': float(current_amount),
                'progress_percentage': min(progress_percentage, 100),
                'remaining_amount': max(float(goal.value) - current_amount, 0),
                'is_completed': current_amount >= goal.value,
                'transaction_count': tag_transactions.count()
            })
        
        return json.dumps({
            'user_id': user_id,
            'goals': goal_progress,
            'summary': {
                'total_goals': len(goal_progress),
                'completed_goals': sum(1 for g in goal_progress if g['is_completed']),
                'total_target': sum(g['target_amount'] for g in goal_progress),
                'total_achieved': sum(g['current_amount'] for g in goal_progress)
            }
        })
        
    except Exception as e:
        return json.dumps({'error': f'Failed to get goal progress: {str(e)}'})


def generate_financial_report(user_id: str, report_type: str, 
                            period: str = "month") -> str:
    """Generate comprehensive financial reports.
    
    Args:
        user_id: The user identifier
        report_type: Type of report (overview, spending, income, net_worth, goals)
        period: Report period (week, month, quarter, year)
        
    Returns:
        Detailed financial report as JSON
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Calculate date range
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
            start_date = end_date - timedelta(days=30)
        
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        if report_type == "overview":
            income = transactions.filter(value__gt=0).aggregate(Sum('value'))['value__sum'] or 0
            expenses = transactions.filter(value__lt=0).aggregate(Sum('value'))['value__sum'] or 0
            
            return json.dumps({
                'report_type': 'overview',
                'period': period,
                'date_range': f"{start_date.date()} to {end_date.date()}",
                'income': float(income),
                'expenses': float(abs(expenses)),
                'net_flow': float(income + expenses),
                'transaction_count': transactions.count(),
                'average_transaction': float((income + expenses) / transactions.count()) if transactions.count() > 0 else 0,
                'generated_at': timezone.now().isoformat()
            })
        
        # Additional report types can be implemented here
        else:
            return json.dumps({'error': f'Report type "{report_type}" not implemented yet'})
            
    except Exception as e:
        return json.dumps({'error': f'Failed to generate report: {str(e)}'}) 