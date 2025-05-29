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
        else:
            return "onboarding"

    def handle_message(self, text: str) -> Tuple[str, Dict]:
        """Route the message and delegate to the appropriate agent."""
        agent_key = self.route(text)
        return self.agents[agent_key].handle_message(text)
