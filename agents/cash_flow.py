"""Cash-flow & budget agent implementation."""

from __future__ import annotations

import json
from typing import Dict, List, Optional, Any

from .base import BaseAgent
from app.models import Message


class CashFlowAgent(BaseAgent):
    """Agent responsible for cash-flow analysis and budgeting.

    Parameters are passed to the LLM via the user message in JSON format.
    Supported ``intent`` values are ``"categorize_txns"`` and ``"create_budget"``.
    When ``create_budget`` is requested the response is expected to match the
    ``BudgetPlan`` schema, otherwise ``CashFlowLedger`` is returned.
    """

    name = "cash_flow"

    # Default schema is the ledger. ``handle_message`` may temporarily switch
    # to ``BudgetPlan.json`` when needed.
    schema_file = "CashFlowLedger.json"

    def handle_message(
        self,
        text: str,
        *,
        intent: Optional[str] = None,
        transactions: Optional[List[Dict]] = None,
        category_map: Optional[Dict[str, str]] = None,
        budget_targets: Optional[Dict[str, float]] = None,
        budget_info: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, Dict]:
        """Call the LLM with structured parameters and return its response."""

        # Determine intent heuristically if not provided
        if intent is None:
            lower = text.lower()
            intent = "create_budget" if "budget" in lower else "categorize_txns"

        params = {
            "intent": intent,
            "transactions": transactions or [],
        }
        if category_map:
            params["category_map"] = category_map
        if budget_targets:
            params["budget_targets"] = budget_targets

        if intent == "create_budget":
            required = [
                "net_income",
                "fixed_essentials",
                "variable_costs",
                "infrequent_costs",
                "savings_investing",
                "balances_today",
                "goals_preferences",
                "logistics",
            ]
            missing = [key for key in required if not budget_info or not budget_info.get(key)]
            if missing:
                return Message.TEXT, {"missing_info": missing}
            params["budget_info"] = budget_info or {}

        # Embed parameters as JSON after the user text so the LLM can parse them
        llm_input = f"{text}\n\n{json.dumps(params)}"

        # Select schema depending on requested intent
        original_schema = self.schema_file
        if intent == "create_budget":
            self.schema_file = "BudgetPlan.json"

        payload = self.generate_payload(llm_input)

        # Validate against the chosen schema and restore the default
        self.validate_payload(payload)
        self.schema_file = original_schema

        return Message.TEXT, payload
