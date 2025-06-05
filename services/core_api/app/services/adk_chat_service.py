"""HTTP-based Chat service that communicates with the FastAPI Agent Service."""

from __future__ import annotations

import logging
import datetime
import os
from typing import Iterable, List, Dict, Optional, Any, Tuple
import requests

from django.contrib.auth import get_user_model
from django.conf import settings

from app.models import Conversation, Message
from myFinance.models import Transaction, TransactionNameTag, TagGoal
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


class ADKChatService:
    """Service layer that communicates with the FastAPI Agent Service via HTTP."""

    def __init__(self) -> None:
        # Get agent service URL from settings or environment
        self.agent_service_url = getattr(settings, 'AGENT_SERVICE_URL', 'http://localhost:8001')
        self.timeout = 30  # 30 second timeout for HTTP requests
        logger.info(f"ADKChatService initialized with agent service URL: {self.agent_service_url}")

    def get_conversation(self, user: get_user_model()) -> Conversation:
        """Get or create conversation for user (maintains Django model persistence)."""
        conversation, _ = Conversation.objects.get_or_create(user=user)
        return conversation

    def history(self, user: get_user_model()) -> Iterable[Message]:
        """Return all messages for the user conversation from Django models."""
        conversation = self.get_conversation(user)
        return conversation.messages.all()

    def send_message(self, user: get_user_model(), text: str) -> Message:
        """Send message to agent service and store results in Django models."""
        conversation = self.get_conversation(user)
        user_id = str(user.id)
        
        # Create user message in Django
        user_message = Message.objects.create(
            conversation=conversation,
            sender=Message.USER,
            content_type=Message.TEXT,
            payload={"text": text},
        )
        logger.info(f"Created user message for user {user_id}: {text}")

        # Try to communicate with agent service
        try:
            content_type, payload = self._call_agent_service(user_id, text, user)
            
            # Create agent message in Django
            agent_message = Message.objects.create(
                conversation=conversation,
                sender=Message.AGENT,
                content_type=Message.TEXT,  # Always store as text for now
                payload=payload,
            )
            logger.info(f"Created agent response for user {user_id}:")
            logger.info(f"Agent response: {payload}")
            
            return agent_message
            
        except Exception as e:
            logger.error(f"Agent service communication failed: {e}")
            return self._create_fallback_response(conversation, user, text)

    def _call_agent_service(self, user_id: str, text: str, user: object) -> Tuple[str, Dict[str, Any]]:
        """Call the Agent Service via HTTP with enhanced context and user token."""
        try:
            # Get user authentication token for the agent service to use
            user_token, created = Token.objects.get_or_create(user=user)
            token_key = user_token.key
            
            if created:
                logger.info(f"Created new token for user {user.id}: {token_key[:10]}...")
            else:
                logger.debug(f"Using existing token for user {user.id}: {token_key[:10]}...")
            
            # Build comprehensive financial context
            context = self._build_financial_context(user)
            
            # Add user token to context so agent service can make API calls
            context["user_token"] = token_key
            context["user_id"] = str(user.id)
            
            # Use token as the primary identifier for session consistency
            # This ensures the agent service uses the same identifier for session management
            logger.info(f"Calling agent service for user {user.id} with token {token_key[:10]}... and message: '{text[:50]}...'")
            
            # Make request to agent service - use token as user_id for session consistency
            response = requests.post(
                f"{self.agent_service_url}/api/chat/send",
                json={
                    "user_id": token_key,  # Use token as user_id for consistent session management
                    "text": text,
                    "context": context
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            logger.info(f"Agent service response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Agent service success - content_type: {data.get('content_type', 'unknown')}")
                logger.debug(f"Agent service payload keys: {list(data.get('payload', {}).keys())}")
                
                # Log session persistence info if available
                metadata = data.get('payload', {}).get('metadata', {})
                if 'session_persisted' in metadata:
                    logger.info(f"Session persistence status: {metadata['session_persisted']}")
                if 'conversation_id' in metadata:
                    logger.info(f"Conversation ID: {metadata['conversation_id']}")
                    
                return data.get("content_type", "text"), data.get("payload", {"text": "No response from agent"})
            else:
                logger.error(f"Agent service returned {response.status_code}: {response.text}")
                return self._create_fallback_response_tuple(user, f"Agent service error {response.status_code}")
                
        except requests.exceptions.Timeout as e:
            logger.error(f"Agent service request timed out: {e}")
            return self._create_fallback_response_tuple(user, "Agent service timed out")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to agent service: {e}")
            return self._create_fallback_response_tuple(user, "Could not connect to agent service")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to call agent service: {e}")
            return self._create_fallback_response_tuple(user, f"Connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling agent service: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return self._create_fallback_response_tuple(user, f"System error: {str(e)}")

    def _build_financial_context(self, user: get_user_model()) -> Dict[str, Any]:
        """Build financial context to send to the agent service."""
        try:
            logger.debug(f"Building financial context for user {user.id}")
            
            # Get user's financial data
            txns, category_map, budget_targets = self.build_financial_context(user)
            budget_inputs = self.get_budget_inputs(user)
            
            context = {
                "transactions": txns[-50:],  # Last 50 transactions to avoid huge payloads
                "category_mapping": category_map,
                "budget_targets": budget_targets,
                "budget_inputs": budget_inputs,
                "user_id": str(user.id),
                "username": user.username
            }
            
            logger.debug(f"Built financial context with {len(context['transactions'])} transactions, {len(category_map)} categories")
            return context
        except Exception as e:
            logger.warning(f"Failed to build financial context for user {user.id}: {e}")
            return {"user_id": str(user.id), "username": user.username}

    def _create_fallback_response_tuple(self, user: object, message: str = "Service temporarily unavailable") -> Tuple[str, Dict[str, Any]]:
        """Create a fallback response tuple when agent service is unavailable."""
        fallback_text = f"I'm currently running in limited mode. {message} Please try again later."
        logger.warning(f"Creating fallback response for user {user.id}: {message}")
        
        return "text", {
            "text": fallback_text,
            "metadata": {
                "error": True,
                "error_message": message,
                "agent_type": "fallback"
            }
        }

    def _create_fallback_response(self, user_or_conversation=None, message: str = "Service temporarily unavailable") -> Tuple[str, Dict[str, Any]]:
        """Create a fallback response when agent service is unavailable."""
        fallback_text = f"I'm currently running in limited mode. {message} Please try again later."
        
        # If it's a conversation and user object, create the message
        if hasattr(user_or_conversation, 'user'):  # It's a conversation
            conversation = user_or_conversation
            user = conversation.user
            text = message
            
            fallback_message = Message.objects.create(
                conversation=conversation,
                sender=Message.AGENT,
                content_type=Message.TEXT,
                payload={"text": fallback_text}
            )
            return fallback_message
        else:
            # It's just a user object or error message, return tuple
            return self._create_fallback_response_tuple(user_or_conversation, message)

    def check_agent_service_health(self) -> bool:
        """Check if the agent service is available."""
        try:
            response = requests.get(
                f"{self.agent_service_url}/api/health/",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Agent service health check failed: {e}")
            return False

    # --------------------------------------------------------------
    # Financial data helpers (preserved from original service)
    # --------------------------------------------------------------

    def get_transactions(
        self,
        user: get_user_model(),
        *,
        start: Optional[datetime.date] = None,
        end: Optional[datetime.date] = None,
    ) -> Iterable[Transaction]:
        """Get user's transactions with optional date filtering."""
        qs = Transaction.objects.filter(user=user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        return qs.order_by("date")

    def serialize_transactions(self, txns: Iterable[Transaction]) -> List[Dict]:
        """Convert transactions to dictionary format for API communication."""
        data: List[Dict] = []
        for txn in txns:
            data.append(
                {
                    "transaction_id": str(txn.pk),
                    "date": txn.date.isoformat(),
                    "description": txn.name,
                    "amount": txn.value,
                    "currency": "ILS",
                    "account_id": str(txn.credential_id or "0"),
                    "category": txn.tag.name if txn.tag else None,
                    "tags": [txn.tag.name] if txn.tag else [],
                }
            )
        return data

    def get_category_map(self, user: get_user_model()) -> Dict[str, str]:
        """Get user's transaction name to category mapping."""
        mapping: Dict[str, str] = {}
        for item in TransactionNameTag.objects.filter(user=user):
            if item.tag:
                mapping[item.transaction_name] = item.tag.name
        return mapping

    def get_budget_targets(self, user: get_user_model()) -> Dict[str, float]:
        """Get user's budget targets by category."""
        return {
            goal.tag.name: goal.value
            for goal in TagGoal.objects.filter(user=user).select_related("tag")
        }

    def build_financial_context(
        self, user: get_user_model()
    ) -> tuple[List[Dict], Dict[str, str], Dict[str, float]]:
        """Build complete financial context for the user."""
        txns = self.serialize_transactions(self.get_transactions(user))
        category_map = self.get_category_map(user)
        budget_targets = self.get_budget_targets(user)
        return txns, category_map, budget_targets

    def get_budget_inputs(self, user: get_user_model()) -> Dict[str, Any]:
        """Get user's budget planning inputs (placeholder implementation)."""
        logger.debug("Retrieving budget inputs for user %s", user)
        return {
            "net_income": {"monthly": 5000, "bonuses": 1000},
            "fixed_essentials": {
                "housing": 1500,
                "debt_payments": 300,
                "utilities": 200,
                "insurance_premiums": 100,
            },
            "variable_costs": {
                "food": 400,
                "transport": 100,
                "personal": 200,
            },
            "infrequent_costs": {
                "car_maintenance": 50,
                "holidays": 100,
                "home_repairs": 50,
            },
            "savings_investing": {
                "pension_plans": 200,
                "brokerage_transfers": 100,
                "emergency_fund": 100,
            },
            "balances_today": {
                "cash": 10000,
                "investments": 5000,
                "loans": 2000,
                "credit_card_balances": 1000,
            },
            "goals_preferences": {
                "timelines": "1yr",
                "risk_tolerance": "medium",
                "lifestyle_priorities": "save for house",
            },
            "logistics": {
                "preferred_currency": "USD",
                "apps": ["excel"],
                "budget_delivery": "email",
            },
        }
