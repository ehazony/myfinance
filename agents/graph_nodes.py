from typing import Dict, Callable

from app.models import Message

from .workflow_state import WorkflowState
from .orchestrator import Orchestrator
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


orchestrator = Orchestrator()

# Instantiate agents
_agent_instances = {
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


def orchestrator_node(state: WorkflowState) -> WorkflowState:
    """Determine which agent should handle the user input."""
    state.next_agent = orchestrator.route(state.user_input)
    state.conversation.append({"agent": "orchestrator", "next": state.next_agent})
    return state


def make_agent_node(name: str) -> Callable[[WorkflowState], WorkflowState]:
    agent = _agent_instances[name]

    def node(state: WorkflowState) -> WorkflowState:
        content_type, payload = agent.handle_message(state.user_input)
        state.conversation.append(
            {"agent": name, "content_type": content_type, "payload": payload}
        )
        state.result = {"content_type": content_type, "payload": payload}
        # After onboarding we demonstrate moving to the reporting agent.
        if name == "onboarding" and content_type != Message.CHART:
            state.next_agent = "reporting"
        else:
            state.done = True
        return state

    return node


AGENT_NODES: Dict[str, Callable[[WorkflowState], WorkflowState]] = {
    name: make_agent_node(name) for name in _agent_instances
}
