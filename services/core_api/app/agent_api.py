"""
Agent Service API endpoints.
Provides structured data access for the agent service with OpenAPI documentation.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from datetime import datetime, date, timedelta
from typing import Dict, Any, List

from myFinance.models import Transaction, TransactionNameTag, TagGoal, Tag, Credential
from app.models import Conversation, Message


# Serializers for OpenAPI documentation
class FinancialContextSerializer(serializers.Serializer):
    """Complete financial context for a user."""
    transactions = serializers.ListField(child=serializers.DictField())
    category_mapping = serializers.DictField()
    budget_targets = serializers.DictField() 
    budget_inputs = serializers.DictField()
    user_id = serializers.CharField()
    username = serializers.CharField()


class TransactionSerializer(serializers.Serializer):
    """Transaction data for agents."""
    transaction_id = serializers.CharField()
    date = serializers.DateField()
    description = serializers.CharField()
    amount = serializers.FloatField()
    currency = serializers.CharField()
    account_id = serializers.CharField()
    category = serializers.CharField(allow_null=True)
    tags = serializers.ListField(child=serializers.CharField())


class BudgetTargetSerializer(serializers.Serializer):
    """Budget target data."""
    category = serializers.CharField()
    target_amount = serializers.FloatField()
    current_spent = serializers.FloatField()
    remaining = serializers.FloatField()
    progress_percentage = serializers.FloatField()


class AccountSummarySerializer(serializers.Serializer):
    """Account summary data."""
    account_id = serializers.CharField()
    account_name = serializers.CharField()
    account_type = serializers.CharField()
    balance = serializers.FloatField(allow_null=True)
    last_transaction_date = serializers.DateField(allow_null=True)
    transaction_count = serializers.IntegerField()


class SpendingAnalysisSerializer(serializers.Serializer):
    """Spending analysis data."""
    total_spent = serializers.FloatField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    top_categories = serializers.ListField(child=serializers.DictField())
    daily_average = serializers.FloatField()
    trend = serializers.CharField()  # "increasing", "decreasing", "stable"


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sender = serializers.CharField()
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    content_type = serializers.CharField(required=False)
    payload = serializers.JSONField(required=False)


class ConversationContextSerializer(serializers.Serializer):
    """User conversation context."""
    conversation_id = serializers.IntegerField(allow_null=True)
    message_count = serializers.IntegerField()
    last_activity = serializers.DateTimeField(allow_null=True)
    recent_topics = serializers.ListField(child=serializers.CharField())
    recent_messages = MessageSerializer(many=True)


# Agent API Views
class AgentFinancialContextView(APIView):
    """
    Get complete financial context for a user.
    Optimized for agent consumption with all necessary financial data.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Financial Context",
        description="Retrieve complete financial context for agent processing including transactions, budgets, and goals.",
        parameters=[
            OpenApiParameter(
                name="limit_transactions",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Limit number of recent transactions (default: 100)",
                default=100
            ),
            OpenApiParameter(
                name="include_future_goals",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Include future financial goals (default: true)",
                default=True
            )
        ],
        responses={200: FinancialContextSerializer}
    )
    def get(self, request):
        user = request.user
        limit = int(request.query_params.get('limit_transactions', 100))
        include_goals = request.query_params.get('include_future_goals', 'true').lower() == 'true'

        # Get recent transactions
        recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:limit]
        transactions_data = []
        for txn in recent_transactions:
            transactions_data.append({
                "transaction_id": str(txn.pk),
                "date": txn.date.isoformat(),
                "description": txn.name,
                "amount": float(txn.value),
                "currency": "ILS",
                "account_id": str(txn.credential_id or "0"),
                "category": txn.tag.name if txn.tag else None,
                "tags": [txn.tag.name] if txn.tag else [],
            })

        # Get category mapping
        category_mapping = {}
        for item in TransactionNameTag.objects.filter(user=user):
            if item.tag:
                category_mapping[item.transaction_name] = item.tag.name

        # Get budget targets
        budget_targets = {}
        for goal in TagGoal.objects.filter(user=user).select_related("tag"):
            budget_targets[goal.tag.name] = float(goal.value)

        # Get budget inputs (placeholder - you can expand this)
        budget_inputs = {
            "net_income": {"monthly": 5000, "bonuses": 1000},
            "fixed_essentials": {"housing": 1500, "utilities": 200},
            "variable_costs": {"food": 400, "transport": 100},
            "savings_goals": {"emergency_fund": 500, "vacation": 200}
        }

        context = {
            "transactions": transactions_data,
            "category_mapping": category_mapping,
            "budget_targets": budget_targets,
            "budget_inputs": budget_inputs,
            "user_id": str(user.id),
            "username": user.username
        }

        return Response(context)


class AgentTransactionsView(APIView):
    """
    Get filtered transactions for agent analysis.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Filtered Transactions",
        description="Retrieve transactions with filtering options for agent analysis.",
        parameters=[
            OpenApiParameter(name="start_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="end_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="category", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="min_amount", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="max_amount", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="limit", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, default=100),
        ],
        responses={200: serializers.ListSerializer(child=TransactionSerializer())}
    )
    def get(self, request):
        user = request.user
        
        # Build query
        queryset = Transaction.objects.filter(user=user)
        
        # Apply filters
        if start_date := request.query_params.get('start_date'):
            queryset = queryset.filter(date__gte=start_date)
        if end_date := request.query_params.get('end_date'):
            queryset = queryset.filter(date__lte=end_date)
        if category := request.query_params.get('category'):
            queryset = queryset.filter(tag__name=category)
        if min_amount := request.query_params.get('min_amount'):
            queryset = queryset.filter(value__gte=float(min_amount))
        if max_amount := request.query_params.get('max_amount'):
            queryset = queryset.filter(value__lte=float(max_amount))
        
        limit = int(request.query_params.get('limit', 100))
        transactions = queryset.order_by('-date')[:limit]
        
        # Serialize data
        data = []
        for txn in transactions:
            data.append({
                "transaction_id": str(txn.pk),
                "date": txn.date.isoformat(),
                "description": txn.name,
                "amount": float(txn.value),
                "currency": "ILS",
                "account_id": str(txn.credential_id or "0"),
                "category": txn.tag.name if txn.tag else None,
                "tags": [txn.tag.name] if txn.tag else [],
            })
        
        return Response(data)


class AgentBudgetAnalysisView(APIView):
    """
    Get budget analysis data for agents.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Budget Analysis",
        description="Retrieve budget vs actual spending analysis for agent insights.",
        parameters=[
            OpenApiParameter(
                name="period", 
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.QUERY,
                description="Analysis period: 'current_month', 'last_month', 'ytd'",
                default="current_month"
            )
        ],
        responses={200: serializers.ListSerializer(child=BudgetTargetSerializer())}
    )
    def get(self, request):
        user = request.user
        period = request.query_params.get('period', 'current_month')
        
        # Determine date range
        today = date.today()
        if period == 'current_month':
            start_date = today.replace(day=1)
            end_date = today
        elif period == 'last_month':
            last_month = today.replace(day=1) - timedelta(days=1)
            start_date = last_month.replace(day=1)
            end_date = last_month
        else:  # ytd
            start_date = today.replace(month=1, day=1)
            end_date = today

        # Get budget targets
        budget_targets = TagGoal.objects.filter(user=user).select_related('tag')
        
        # Calculate actual spending by category
        spending_by_category = {}
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date,
            tag__isnull=False
        ).values('tag__name').annotate(total=Sum('value'))
        
        for item in transactions:
            spending_by_category[item['tag__name']] = abs(float(item['total']))

        # Build analysis
        analysis = []
        for target in budget_targets:
            category = target.tag.name
            target_amount = float(target.value)
            current_spent = spending_by_category.get(category, 0.0)
            remaining = max(0, target_amount - current_spent)
            progress = (current_spent / target_amount * 100) if target_amount > 0 else 0
            
            analysis.append({
                "category": category,
                "target_amount": target_amount,
                "current_spent": current_spent,
                "remaining": remaining,
                "progress_percentage": round(progress, 2)
            })

        return Response(analysis)


class AgentAccountSummaryView(APIView):
    """
    Get account summary for agent analysis.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Account Summary", 
        description="Retrieve account balances and transaction counts for agent insights.",
        responses={200: serializers.ListSerializer(child=AccountSummarySerializer())}
    )
    def get(self, request):
        user = request.user
        
        accounts = Credential.objects.filter(user=user)
        summary = []
        
        for account in accounts:
            # Get transaction stats for this account
            transactions = Transaction.objects.filter(user=user, credential=account)
            transaction_count = transactions.count()
            last_transaction = transactions.order_by('-date').first()
            
            summary.append({
                "account_id": str(account.id),
                "account_name": account.name,
                "account_type": account.type.name if account.type else "Unknown",
                "balance": None,  # Add balance logic if available
                "last_transaction_date": last_transaction.date.isoformat() if last_transaction else None,
                "transaction_count": transaction_count
            })
        
        return Response(summary)


class AgentConversationContextView(APIView):
    """
    Get conversation context for maintaining agent memory.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Conversation Context",
        description="Retrieve conversation history and context for agent memory.",
        responses={200: ConversationContextSerializer}
    )
    def get(self, request):
        user = request.user
        # Get conversation
        conversation = None
        try:
            conversation = Conversation.objects.get(user=user)
        except Conversation.DoesNotExist:
            return Response({
                "conversation_id": None,
                "message_count": 0,
                "last_activity": None,
                "recent_topics": [],
                "recent_messages": []
            })
        messages = conversation.messages.all()
        message_count = messages.count()
        last_message = messages.order_by('-timestamp').first()
        # Extract recent topics (simplified)
        recent_topics = []
        for message in messages.filter(sender='user').order_by('-timestamp')[:5]:
            text = message.payload.get('text', '')
            if len(text) > 10:  # Basic topic extraction
                recent_topics.append(text[:50] + "..." if len(text) > 50 else text)
        # Get recent messages (last 20)
        recent_messages_qs = messages.order_by('-timestamp')[:20]
        recent_messages = []
        for m in reversed(recent_messages_qs):  # reverse to chronological order
            recent_messages.append({
                "id": m.id,
                "sender": m.sender,
                "content": m.payload.get('text', ''),
                "timestamp": m.timestamp,
                "content_type": m.content_type if hasattr(m, 'content_type') else '',
                "payload": m.payload,
            })
        return Response({
            "conversation_id": conversation.id,
            "message_count": message_count,
            "last_activity": last_message.timestamp if last_message else None,
            "recent_topics": recent_topics,
            "recent_messages": recent_messages
        }) 