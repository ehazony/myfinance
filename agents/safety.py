from .base import BaseAgent
from app.models import Message


class SafetyAgent(BaseAgent):
    name = "safety"
    schema_file = "SafetyLayer.json"

    def handle_message(self, text: str):
        payload = {
            "safety_id": "00000000-0000-0000-0000-000000000000",
            "snapshot_id": "00000000-0000-0000-0000-000000000000",
            "emergency_months_required": 3,
            "emergency_months_current": 0,
            "insurance_coverages": [
                {
                    "policy_id": "00000000-0000-0000-0000-000000000000",
                    "coverage_type": "other",
                    "coverage_amount": 0,
                    "premium": 0,
                    "status": "active"
                }
            ]
        }
        self.validate_payload(payload)
        return Message.TEXT, payload
