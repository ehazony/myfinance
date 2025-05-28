from .base import BaseAgent
from app.models import Message


class ReportingAgent(BaseAgent):
    name = "reporting"
    schema_file = "Report.json"

    def handle_message(self, text: str):
        payload = {
            "report_id": "00000000-0000-0000-0000-000000000000",
            "type": "net_worth",
            "generated_at": "2024-01-01T00:00:00Z",
            "source_refs": [],
            "chart_url": "https://example.com/chart.png",
            "summary_markdown": "Example report"
        }
        self.validate_payload(payload)
        return Message.CHART, payload
