import base64
import uuid
from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest
import plotly.graph_objects as go

from agents.reporting import ReportingAgent
from app.models import Message


class TestReportingAgent:
    """Test suite for ReportingAgent with Plotly chart generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = ReportingAgent()

    def test_agent_initialization(self):
        """Test that the agent initializes with correct properties."""
        assert self.agent.name == "reporting"
        assert self.agent.schema_file == "Report.json"

    def test_handle_message_returns_chart_message(self):
        """Test that handle_message returns a CHART message type."""
        content_type, payload = self.agent.handle_message("show me a chart")
        
        assert content_type == Message.CHART
        assert isinstance(payload, dict)

    def test_payload_structure_compliance(self):
        """Test that the generated payload follows the Report schema structure."""
        _, payload = self.agent.handle_message("generate expense chart")
        
        # Test required fields are present
        required_fields = ["report_id", "type", "generated_at", "source_refs"]
        for field in required_fields:
            assert field in payload, f"Required field '{field}' missing from payload"
        
        # Test field types and formats
        assert isinstance(payload["report_id"], str)
        assert isinstance(payload["type"], str)
        assert isinstance(payload["generated_at"], str)
        assert isinstance(payload["source_refs"], list)
        
        # Test UUID format for report_id
        uuid_obj = uuid.UUID(payload["report_id"])  # Should not raise ValueError
        assert str(uuid_obj) == payload["report_id"]
        
        # Test ISO datetime format
        datetime.fromisoformat(payload["generated_at"])  # Should not raise ValueError

    def test_chart_url_format(self):
        """Test that chart_url is properly formatted as base64 data URL."""
        _, payload = self.agent.handle_message("show me expenses")
        
        chart_url = payload.get("chart_url")
        assert chart_url is not None
        assert chart_url.startswith("data:image/png;base64,")
        
        # Extract and validate base64 data
        base64_data = chart_url.split(",")[1]
        assert len(base64_data) > 0
        
        # Test that base64 data can be decoded
        try:
            base64.b64decode(base64_data)
        except Exception as e:
            pytest.fail(f"Invalid base64 data: {e}")

    def test_generate_sample_chart_returns_base64(self):
        """Test that _generate_sample_chart returns valid base64 string."""
        base64_string = self.agent._generate_sample_chart()
        
        assert isinstance(base64_string, str)
        assert len(base64_string) > 0
        
        # Test base64 decoding
        try:
            decoded_bytes = base64.b64decode(base64_string)
            assert len(decoded_bytes) > 0
            # PNG files start with specific bytes
            assert decoded_bytes[:4] == b'\x89PNG'
        except Exception as e:
            pytest.fail(f"Failed to decode base64 chart data: {e}")

    def test_chart_generation_with_plotly_data(self):
        """Test that the chart contains expected financial data."""
        base64_string = self.agent._generate_sample_chart()
        
        # Decode the image to verify it's a valid PNG
        image_data = base64.b64decode(base64_string)
        
        # Check PNG signature
        assert image_data[:8] == b'\x89PNG\r\n\x1a\n'
        
        # Ensure image has reasonable size (not empty/tiny)
        assert len(image_data) > 1000  # Should be larger than 1KB for a real chart

    @patch('plotly.graph_objects.Figure.to_image')
    def test_chart_export_error_handling(self, mock_to_image):
        """Test error handling when chart export fails."""
        # Mock Plotly export to raise an exception
        mock_to_image.side_effect = Exception("Export failed")
        
        with pytest.raises(Exception):
            self.agent._generate_sample_chart()

    def test_sample_data_integrity(self):
        """Test that the sample data used in charts is reasonable."""
        # This test inspects the sample data by calling the method
        # In a real scenario, this would test against actual financial data
        
        # The sample chart method should use realistic financial categories
        base64_string = self.agent._generate_sample_chart()
        assert len(base64_string) > 0
        
        # We can't easily inspect the chart content without additional tools,
        # but we can ensure the method completes successfully

    def test_summary_markdown_present(self):
        """Test that summary_markdown is included in the response."""
        _, payload = self.agent.handle_message("show budget breakdown")
        
        assert "summary_markdown" in payload
        assert isinstance(payload["summary_markdown"], str)
        assert len(payload["summary_markdown"]) > 0
        assert "Monthly Expenses by Category" in payload["summary_markdown"]

    def test_different_input_messages(self):
        """Test agent handles different input messages consistently."""
        test_messages = [
            "show me a chart",
            "generate expense report",
            "budget visualization",
            "financial graph",
            "chart please"
        ]
        
        for message in test_messages:
            content_type, payload = self.agent.handle_message(message)
            
            assert content_type == Message.CHART
            assert "chart_url" in payload
            assert payload["chart_url"].startswith("data:image/png;base64,")

    def test_future_method_stubs(self):
        """Test that future implementation methods exist but return None."""
        assert self.agent._generate_net_worth_trend([]) is None
        assert self.agent._generate_portfolio_allocation([]) is None
        assert self.agent._generate_debt_payoff_timeline([]) is None

    @patch('agents.reporting.uuid.uuid4')
    def test_unique_report_ids(self, mock_uuid):
        """Test that each report gets a unique ID."""
        # Mock uuid to return different values
        mock_uuid.side_effect = [
            MagicMock(spec=uuid.UUID, __str__=lambda x: "id-1"),
            MagicMock(spec=uuid.UUID, __str__=lambda x: "id-2")
        ]
        
        _, payload1 = self.agent.handle_message("chart 1")
        _, payload2 = self.agent.handle_message("chart 2")
        
        assert payload1["report_id"] != payload2["report_id"]

    def test_chart_dimensions_and_quality(self):
        """Test that generated charts have appropriate dimensions and quality."""
        base64_string = self.agent._generate_sample_chart()
        image_data = base64.b64decode(base64_string)
        
        # PNG files should be reasonably sized for a 800x500 chart
        # At 2x scale (1600x1000), expect at least 50KB for a quality chart
        assert len(image_data) > 50000, "Chart image seems too small, may be low quality"

    def test_agent_system_prompt_exists(self):
        """Test that the agent can load its system prompt."""
        prompt = self.agent.system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "Reporting & Visualisation Agent" in prompt

    def test_schema_loading(self):
        """Test that the agent can load its JSON schema."""
        schema = self.agent.load_schema()
        assert isinstance(schema, dict)
        assert "$schema" in schema or "type" in schema  # Basic schema validation 