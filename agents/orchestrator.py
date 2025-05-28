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

    def handle_message(self, text: str) -> Tuple[str, Dict]:
        lower = text.lower()
        if "chart" in lower or "graph" in lower:
            return self.agents["reporting"].handle_message(text)
        elif "goal" in lower:
            return self.agents["goal_setting"].handle_message(text)
        elif "safety" in lower:
            return self.agents["safety"].handle_message(text)
        elif "tax" in lower:
            return self.agents["tax_pension"].handle_message(text)
        elif "invest" in lower:
            return self.agents["investment"].handle_message(text)
        elif "cash" in lower:
            return self.agents["cash_flow"].handle_message(text)
        else:
            return self.agents["onboarding"].handle_message(text)
