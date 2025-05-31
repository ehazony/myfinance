import logging
from typing import Tuple, Dict
import json
from pathlib import Path

from app.models import Message

from .base import BaseAgent
from .onboarding import OnboardingAgent
from .cash_flow import CashFlowAgent
from .goal_setting import GoalSettingAgent
from .safety import SafetyAgent
from .tax_pension import TaxPensionAgent
from .investment import InvestmentAgent
from .reporting import ReportingAgent
from .conversation import ConversationAgent
from .debt_strategy import DebtStrategyAgent
from .reminder_scheduler import ReminderSchedulerAgent
from .compliance_privacy import CompliancePrivacyAgent
from .manifest import load_manifest

logger = logging.getLogger(__name__)


class Orchestrator(BaseAgent):
    """Router agent backed by an LLM with heuristic fallback."""

    name = "orchestrator"

    def __init__(self, manifest_path: str | None = None):
        self.manifest = load_manifest(manifest_path)
        self.agents = {
            "conversation": ConversationAgent(manifest_path),
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
        # Map human-readable agent names from the manifest to keys
        self.agent_name_map = {
            entry["name"]: entry["key"] for entry in self.manifest.get("agents", [])
        }

    def system_prompt(self) -> str:
        base = super().system_prompt()
        
        # Load intent mapping from intents.json
        intents_path = Path(__file__).parent / "prompt" / "system_prompt" / "intents.json"
        intent_mapping = {}
        if intents_path.exists():
            with open(intents_path) as f:
                intent_mapping = json.load(f)
        
        # Build the intent → agent mapping table
        intent_map_lines = []
        for intent, config in intent_mapping.items():
            agent = config.get("agent", "Unknown")
            intent_map_lines.append(f'"{intent}" → {agent}')
        
        intent_map_section = "\n".join(intent_map_lines) if intent_map_lines else "No intent mappings defined"
        
        # Build capabilities section
        caps = [
            {"name": a["name"], "user_friendly": a.get("user_friendly", "")}
            for a in self.manifest.get("agents", [])
        ]
        manifest_obj = json.dumps({"capabilities": caps}, ensure_ascii=False, indent=2)
        
        # Replace the empty INTENT → AGENT MAP section and append capabilities
        full_prompt = base.replace(
            "## INTENT → AGENT MAP\n\n```\n```", 
            f"## INTENT → AGENT MAP\n\n{intent_map_section}\n\n## AVAILABLE AGENTS\n\n{manifest_obj}"
        )
        
        return full_prompt

    def _heuristic_route(self, text: str) -> str:
        """Fallback routing logic when LLM output is missing."""
        logger.debug("Heuristic routing for text: %s", text)
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
        if any(word in lower for word in ["help", "hello", "hi", "greet", "clarify", "explain", "joke"]):
            return "conversation"
        return "onboarding"

    def route(self, text: str, payload: Dict | None = None) -> str:
        """Return which agent should handle the text via the LLM."""
        if payload is None:
            payload = self.generate_payload(text)
        logger.debug("Routing message: '%s' with payload: %s", text, payload)

        agent_name = payload.get("agent")
        agent_key = self.agent_name_map.get(agent_name)

        if not agent_key:
            agent_key = self._heuristic_route(text)
            logger.debug("Heuristic selected agent: %s", agent_key)

        logger.debug("Final routed agent: %s", agent_key)
        return agent_key

    def handle_message(self, text: str, **context) -> Tuple[str, Dict]:
        """Route the message and delegate to the appropriate agent."""
        payload = self.generate_payload(text)
        logger.debug("Orchestrator payload: %s", payload)

        agent_name = payload.get("agent")
        intent = payload.get("intent")
        params = payload.get("params", {})

        agent_key = self.agent_name_map.get(agent_name)

        if not agent_key:
            agent_key = self._heuristic_route(text)
        logger.debug("Delegating to agent: %s", agent_key)

        kwargs = {}

        if agent_key == "cash_flow":
            if intent:
                kwargs["intent"] = intent
            kwargs.update(
                transactions=context.get("transactions"),
                category_map=context.get("category_map"),
                budget_targets=context.get("budget_targets"),
            )
        elif agent_key == "conversation":
            # Pass intent and params to conversation agent for direct user interactions
            if intent:
                kwargs["intent"] = intent
                kwargs["params"] = params
        elif intent:
            # Other agents currently ignore intent
            pass

        content_type, payload = self.agents[agent_key].handle_message(text, **kwargs)
        logger.debug("Agent %s returned %s", agent_key, content_type)

        if agent_key != "conversation":
            content_type, payload = self.agents["conversation"].handle_message(
                text, source="Data", agent=agent_key, payload=payload
            )

        return content_type, payload
