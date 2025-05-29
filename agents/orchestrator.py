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


class Orchestrator:
    """Very simple router that delegates to specific agents."""

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

    def route(self, text: str) -> str:
        """Return which agent should handle the text."""
        lower = text.lower()
        if "chart" in lower or "graph" in lower:
            return "reporting"
        elif "goal" in lower:
            return "goal_setting"
        elif "safety" in lower:
            return "safety"
        elif "tax" in lower:
            return "tax_pension"
        elif "invest" in lower:
            return "investment"
        elif "cash" in lower:
            return "cash_flow"
        elif any(word in lower for word in ["debt", "payoff", "refinance", "loan"]):
            return "debt_strategy"
        elif any(word in lower for word in ["remind", "schedule", "recurring", "check"]):
            return "reminder_scheduler"
        elif any(word in lower for word in ["privacy", "delete", "scrub", "access", "audit"]):
            return "compliance_privacy"
        else:
            return "onboarding"

    def handle_message(self, text: str) -> Tuple[str, Dict]:
        """Route the message and delegate to the appropriate agent."""
        agent_key = self.route(text)
        return self.agents[agent_key].handle_message(text)
