import json
from typing import Tuple, Dict

from app.models import Message

from .base import BaseAgent
from .onboarding import OnboardingAgent
from .cash_flow import CashFlowAgent
from .goal_setting import GoalSettingAgent
from .safety import SafetyAgent
from .tax_pension import TaxPensionAgent
from .investment import InvestmentAgent
from .reporting import ReportingAgent
from .debt_strategy import DebtStrategyAgent
from .reminder_scheduler import ReminderSchedulerAgent
from .compliance_privacy import CompliancePrivacyAgent


class Orchestrator(BaseAgent):
    """Router agent backed by an LLM with heuristic fallback."""

    name = "orchestrator"

    def __init__(self):
        self.agents = {
            "onboarding": OnboardingAgent(),
            "cash_flow": CashFlowAgent(),
            "goal_setting": GoalSettingAgent(),
            "safety": SafetyAgent(),
            "tax_pension": TaxPensionAgent(),
            "investment": InvestmentAgent(),
            "reporting": ReportingAgent(),
            "debt_strategy": DebtStrategyAgent(),
            "reminder_scheduler": ReminderSchedulerAgent(),
            "compliance_privacy": CompliancePrivacyAgent(),
        }
        # Map human-readable agent names from the system prompt to keys
        self.agent_name_map = {
            "Onboarding & Baseline": "onboarding",
            "Cash-Flow & Budget": "cash_flow",
            "Goal-Setting": "goal_setting",
            "Safety-Layer": "safety",
            "Tax & Pension Optimiser": "tax_pension",
            "Investment Architect": "investment",
            "Reporting & Visualisation": "reporting",
            "Debt-Strategy": "debt_strategy",
            "Review & Reminder Scheduler": "reminder_scheduler",
            "Compliance & Privacy": "compliance_privacy",
        }

    def _heuristic_route(self, text: str) -> str:
        """Fallback routing logic when LLM output is missing."""
        lower = text.lower()
        if "chart" in lower or "graph" in lower:
            return "reporting"
        if "goal" in lower:
            return "goal_setting"
        if "safety" in lower:
            return "safety"
        if "tax" in lower:
            return "tax_pension"
        if "invest" in lower:
            return "investment"
        if "cash" in lower:
            return "cash_flow"
        if any(word in lower for word in ["debt", "payoff", "refinance", "loan"]):
            return "debt_strategy"
        if any(word in lower for word in ["remind", "schedule", "recurring", "check"]):
            return "reminder_scheduler"
        if any(word in lower for word in ["privacy", "delete", "scrub", "access", "audit"]):
            return "compliance_privacy"
        return "onboarding"

    def route(self, text: str, payload: Dict | None = None) -> str:
        """Return which agent should handle the text via the LLM."""
        if payload is None:
            payload = self.generate_payload(text)

        agent_name = payload.get("agent")
        agent_key = self.agent_name_map.get(agent_name)

        if not agent_key:
            agent_key = self._heuristic_route(text)

        return agent_key

    def handle_message(self, text: str, **context) -> Tuple[str, Dict]:
        """Route the message and delegate to the appropriate agent."""
        payload = self.generate_payload(text)

        agent_name = payload.get("agent")
        intent = payload.get("intent")
        params = payload.get("params", {})

        agent_key = self.agent_name_map.get(agent_name)

        # If the LLM determines the orchestrator should respond directly
        if agent_key is None and agent_name == "Orchestrator":
            if intent == "clarify":
                question = params.get("question", "Could you clarify?")
                return Message.TEXT, {"text": question}
            if intent == "fallback":
                message = params.get("message", text)
                return Message.TEXT, {"text": message}

        if not agent_key:
            agent_key = self._heuristic_route(text)

        kwargs = {}

        if agent_key == "cash_flow":
            if intent:
                kwargs["intent"] = intent
            kwargs.update(
                transactions=context.get("transactions"),
                category_map=context.get("category_map"),
                budget_targets=context.get("budget_targets"),
            )
        elif intent:
            # Other agents currently ignore intent
            pass

        return self.agents[agent_key].handle_message(text, **kwargs)
