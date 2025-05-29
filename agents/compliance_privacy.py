from .base import BaseAgent
from app.models import Message


class CompliancePrivacyAgent(BaseAgent):
    name = "compliance_privacy"
    schema_file = "SecurityAuditRecord.json"

    def handle_message(self, text: str):
        payload = self.generate_payload(text)
        self.validate_payload(payload)
        return Message.TEXT, payload 