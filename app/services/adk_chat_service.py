"""Chat service using the ADK runner and root agent."""

from __future__ import annotations

import asyncio
import logging
import datetime
import os
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Any

from django.contrib.auth import get_user_model

from app.models import Conversation, Message
from myFinance.models import Transaction, TransactionNameTag, TagGoal

# Load environment variables from agents_adk/.env file
env_file = Path(__file__).parent.parent.parent / 'agents_adk' / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

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

    def history(self, user: get_user_model()) -> Iterable[Message]:
        """Return all messages for the user conversation."""
        conversation = self.get_conversation(user)
        return conversation.messages.all()

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
        async def ensure_session_async():
            # Check if session already exists
            existing_session = await self.session_service.get_session(
                app_name="FinanceAgent", 
                user_id=user_id, 
                session_id=session_id
            )
            
            # Only create if it doesn't exist
            if not existing_session:
                await self.session_service.create_session(
                    app_name="FinanceAgent", 
                    user_id=user_id, 
                    session_id=session_id
                )
                logger.info(f"🆕 Created new session for user {user_id}, session {session_id}")
            else:
                logger.info(f"♻️  Using existing session for user {user_id}, session {session_id} (events: {len(existing_session.events)})")
        
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # When called inside async context, use run_until_complete
                loop.run_until_complete(ensure_session_async())
            else:
                # Loop exists but not running, use asyncio.run
                asyncio.run(ensure_session_async())
        except RuntimeError:
            # No event loop in current thread (Django request thread), create one
            asyncio.run(ensure_session_async())

    def send_message(self, user: get_user_model(), text: str) -> Message:
        conversation = self.get_conversation(user)
        user_id = str(user.id)
        session_id = str(conversation.id)
        
        # Create user message in Django
        Message.objects.create(
            conversation=conversation,
            sender=Message.USER,
            content_type=Message.TEXT,
            payload={"text": text},
        )

        self._ensure_session(user_id, session_id)

        # DEBUG: Log session state BEFORE processing
        logger.info(f"🔍 DEBUG: Processing message '{text}' for user {user_id}, session {session_id}")
        asyncio.run(self._debug_session_state(user_id, session_id, "BEFORE"))

        user_message = types.Content(role="user", parts=[types.Part(text=text)])
        events = self.runner.run(user_id=user_id, session_id=session_id, new_message=user_message)
        
        final_text = None
        for event in events:
            # DEBUG: Log each event as it comes
            logger.info(f"📨 EVENT: {type(event).__name__} - Author: {getattr(event, 'author', 'N/A')} - Is_final: {getattr(event, 'is_final_response', lambda: False)()}")
            
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text"):
                        final_text = part.text
            if getattr(event, "is_final_response", lambda: False)():
                if event.content and event.content.parts:
                    final_text = event.content.parts[0].text
                break
        
        # DEBUG: Log session state AFTER processing
        asyncio.run(self._debug_session_state(user_id, session_id, "AFTER"))
        
        if final_text is None:
            final_text = ""

        agent_msg = Message.objects.create(
            conversation=conversation,
            sender=Message.AGENT,
            content_type=Message.TEXT,
            payload={"text": final_text},
        )
        return agent_msg

    async def _debug_session_state(self, user_id: str, session_id: str, stage: str) -> None:
        """Debug helper to log session state and events."""
        try:
            session = await self.session_service.get_session(
                app_name="FinanceAgent", 
                user_id=user_id, 
                session_id=session_id
            )
            
            if not session:
                logger.warning(f"🚨 {stage}: No session found for user {user_id}, session {session_id}")
                return
            
            logger.info(f"🔍 {stage} SESSION DEBUG:")
            logger.info(f"  📋 Session ID: {session.id}")
            logger.info(f"  👤 User ID: {session.user_id}")
            logger.info(f"  📊 Total Events: {len(session.events)}")
            
            # Log recent events (last 5)
            recent_events = list(session.events)[-5:] if session.events else []
            logger.info(f"  📜 Recent Events ({len(recent_events)}):")
            
            for i, event in enumerate(recent_events):
                event_type = type(event).__name__
                author = getattr(event, 'author', 'N/A')
                event_id = getattr(event, 'id', 'N/A')
                timestamp = getattr(event, 'timestamp', 'N/A')
                
                logger.info(f"    {i+1}. Type: {event_type} | Author: {author} | ID: {event_id} | Time: {timestamp}")
                
                # Log content preview if available
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts[:1]:  # Just first part
                        if hasattr(part, 'text') and part.text:
                            preview = part.text[:100] + "..." if len(part.text) > 100 else part.text
                            logger.info(f"      Content: {preview}")
            
            # Log agent information
            logger.info(f"  🤖 Root Agent: {self.runner.agent.name}")
            logger.info(f"  🔍 Available Sub-agents: {[agent.name for agent in getattr(self.runner.agent, 'sub_agents', [])]}")
            
            # Try to determine which agent would be selected
            # We can't directly call _find_agent_to_run, but we can simulate the logic
            logger.info(f"  🎯 Agent Selection Analysis:")
            if session.events:
                for event in reversed(session.events):
                    if getattr(event, 'author', None) != 'user':
                        logger.info(f"    Last non-user event: {type(event).__name__} by {getattr(event, 'author', 'N/A')}")
                        break
                else:
                    logger.info(f"    No non-user events found")
            else:
                logger.info(f"    No events in session")
                
        except Exception as e:
            logger.error(f"🚨 Error in session debug: {e}")
            import traceback
            logger.error(traceback.format_exc())
