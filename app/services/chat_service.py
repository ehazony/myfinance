"""Backend chat service providing ORM integration for the agent flow."""

from __future__ import annotations

import datetime
import logging
from typing import Iterable, List, Dict, Optional, Any

from django.contrib.auth import get_user_model

from app.models import Conversation, Message
from myFinance.models import Transaction, TransactionNameTag, TagGoal
from agents.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


class ChatService:
    """Service layer bridging the agent flow and the Django ORM."""

    def __init__(self, orchestrator: Orchestrator | None = None) -> None:
        self.orchestrator = orchestrator or Orchestrator()

    def get_conversation(self, user: get_user_model()) -> Conversation:
        """Return existing conversation for user or create one."""
        conversation, created = Conversation.objects.get_or_create(user=user)
        if created:
            logger.debug("Created new conversation for user %s", user)
        else:
            logger.debug("Loaded conversation %s for user %s", conversation.pk, user)
        return conversation

    def history(self, user: get_user_model()) -> Iterable[Message]:
        """Return all messages for the user conversation."""
        conversation = self.get_conversation(user)
        return conversation.messages.all()

    # ------------------------------------------------------------------
    # ORM helpers
    # ------------------------------------------------------------------

    def get_transactions(
        self,
        user: get_user_model(),
        *,
        start: Optional[datetime.date] = None,
        end: Optional[datetime.date] = None,
    ) -> Iterable[Transaction]:
        """Return transactions for the user in the optional date range."""
        qs = Transaction.objects.filter(user=user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        return qs.order_by("date")

    def serialize_transactions(self, txns: Iterable[Transaction]) -> List[Dict]:
        """Convert transactions to a list of dicts for agents."""
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
        """Return mapping of merchant/description to category."""
        mapping: Dict[str, str] = {}
        for item in TransactionNameTag.objects.filter(user=user):
            if item.tag:
                mapping[item.transaction_name] = item.tag.name
        return mapping

    def get_budget_targets(self, user: get_user_model()) -> Dict[str, float]:
        """Return budget target values per tag name."""
        return {
            goal.tag.name: goal.value
            for goal in TagGoal.objects.filter(user=user).select_related("tag")
        }

    def build_financial_context(
        self, user: get_user_model()
    ) -> tuple[List[Dict], Dict[str, str], Dict[str, float]]:
        """Return serialized transactions, category map and budget targets."""
        txns = self.serialize_transactions(self.get_transactions(user))
        category_map = self.get_category_map(user)
        budget_targets = self.get_budget_targets(user)
        logger.debug("Built financial context for user %s", user)
        return txns, category_map, budget_targets

    # ------------------------------------------------------------------
    # Budget input placeholders
    # ------------------------------------------------------------------

    def get_budget_inputs(self, user: get_user_model()) -> Dict[str, Any]:
        """Return additional budget information for the CashFlow agent.

        This placeholder implementation returns hard-coded values so the
        cash-flow agent can produce a budget without prompting the user
        for every field.  Real deployments would fetch these details
        from the user's profile or recently submitted forms.
        """

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

    def send_message(self, user: get_user_model(), text: str) -> Message:
        """Persist the user text, run the agent flow and store the reply."""
        conversation = self.get_conversation(user)
        Message.objects.create(
            conversation=conversation,
            sender=Message.USER,
            content_type=Message.TEXT,
            payload={"text": text},
        )

        txns, category_map, budget_targets = self.build_financial_context(user)
        budget_info = self.get_budget_inputs(user)

        logger.debug("Sending message to orchestrator: '%s'", text)
        content_type, payload = self.orchestrator.handle_message(
            text,
            transactions=txns,
            category_map=category_map,
            budget_targets=budget_targets,
            budget_info=budget_info,
        )
        logger.debug("Orchestrator returned content_type=%s", content_type)
        agent_msg = Message.objects.create(
            conversation=conversation,
            sender=Message.AGENT,
            content_type=content_type,
            payload=payload,
        )
        return agent_msg
