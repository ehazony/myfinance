"""Chat service using the ADK runner and root agent."""

from __future__ import annotations

import asyncio
import logging
import datetime
from typing import Iterable, List, Dict, Optional, Any

from django.contrib.auth import get_user_model

from app.models import Conversation, Message
from myFinance.models import Transaction, TransactionNameTag, TagGoal

from agents_adk.agent import root_agent

try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
except Exception:  # pragma: no cover - ADK may not be installed during tests
    Runner = None  # type: ignore
    InMemorySessionService = None  # type: ignore
    types = None  # type: ignore


logger = logging.getLogger(__name__)


class ADKChatService:
    """Service layer using the ADK runner to process messages."""

    def __init__(self) -> None:
        if Runner is None:
            raise ImportError("google-adk is required for ADKChatService")
        self.session_service = InMemorySessionService()
        self.runner = Runner(agent=root_agent, app_name="FinanceAgent", session_service=self.session_service)

    def get_conversation(self, user: get_user_model()) -> Conversation:
        conversation, _ = Conversation.objects.get_or_create(user=user)
        return conversation

    # --------------------------------------------------------------
    # ORM helpers (copied from legacy service)
    # --------------------------------------------------------------

    def get_transactions(
        self,
        user: get_user_model(),
        *,
        start: Optional[datetime.date] = None,
        end: Optional[datetime.date] = None,
    ) -> Iterable[Transaction]:
        qs = Transaction.objects.filter(user=user)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        return qs.order_by("date")

    def serialize_transactions(self, txns: Iterable[Transaction]) -> List[Dict]:
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
        mapping: Dict[str, str] = {}
        for item in TransactionNameTag.objects.filter(user=user):
            if item.tag:
                mapping[item.transaction_name] = item.tag.name
        return mapping

    def get_budget_targets(self, user: get_user_model()) -> Dict[str, float]:
        return {
            goal.tag.name: goal.value
            for goal in TagGoal.objects.filter(user=user).select_related("tag")
        }

    def build_financial_context(
        self, user: get_user_model()
    ) -> tuple[List[Dict], Dict[str, str], Dict[str, float]]:
        txns = self.serialize_transactions(self.get_transactions(user))
        category_map = self.get_category_map(user)
        budget_targets = self.get_budget_targets(user)
        return txns, category_map, budget_targets

    def get_budget_inputs(self, user: get_user_model()) -> Dict[str, Any]:
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

    def _ensure_session(self, user_id: str, session_id: str) -> None:
        if not asyncio.get_event_loop().is_running():
            asyncio.run(self.session_service.create_session(app_name="FinanceAgent", user_id=user_id, session_id=session_id))
        else:
            # When called inside async context
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.session_service.create_session(app_name="FinanceAgent", user_id=user_id, session_id=session_id))

    def send_message(self, user: get_user_model(), text: str) -> Message:
        conversation = self.get_conversation(user)
        Message.objects.create(
            conversation=conversation,
            sender=Message.USER,
            content_type=Message.TEXT,
            payload={"text": text},
        )

        self._ensure_session(str(user.id), str(conversation.id))

        user_message = types.Content(role="user", parts=[types.Part(text=text)])
        events = self.runner.run(user_id=str(user.id), session_id=str(conversation.id), new_message=user_message)
        final_text = None
        for event in events:
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text"):
                        final_text = part.text
            if getattr(event, "is_final_response", lambda: False)():
                if event.content and event.content.parts:
                    final_text = event.content.parts[0].text
                break
        if final_text is None:
            final_text = ""

        agent_msg = Message.objects.create(
            conversation=conversation,
            sender=Message.AGENT,
            content_type=Message.TEXT,
            payload={"text": final_text},
        )
        return agent_msg
