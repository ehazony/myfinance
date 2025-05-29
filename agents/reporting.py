import base64
import io
import uuid
from datetime import datetime
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .base import BaseAgent
from app.models import Message


class ReportingAgent(BaseAgent):
    """
    Reporting & Visualization Agent using Plotly for beautiful financial charts.
    
    CURRENT IMPLEMENTATION: Plotly + PNG export + base64 encoding
    
    FUTURE OPTIONS TO CONSIDER:
    1. Interactive HTML charts: Use fig.to_html() for interactive charts in iframes
    2. SVG export: Use fig.to_image(format="svg") for scalable vector graphics
    3. Chart.js integration: Use pyecharts or similar for web-native charts
    4. Real-time updates: WebSocket integration for live chart updates
    5. Dashboard mode: Multi-chart layouts using plotly.subplots
    """
    
    name = "reporting"
    schema_file = "Report.json"

    def handle_message(self, text: str):
        """Generate charts based on user request."""
        
        lower = text.lower()
        chart_data = self._generate_sample_chart()
        categories = [
            "Food & Dining", "Transportation", "Shopping", "Entertainment",
            "Bills & Utilities", "Healthcare", "Travel", "Other",
        ]
        amounts = [1200, 800, 600, 400, 900, 300, 500, 200]
        if "chart data" in lower:
            payload = {
                "report_id": str(uuid.uuid4()),
                "type": "budget",
                "generated_at": datetime.now().isoformat(),
                "source_refs": ["sample_data"],
                "labels": categories,
                "values": amounts,
                "summary_markdown": "## Monthly Expenses by Category\n\nThis chart shows your spending breakdown by category for the selected period.",
            }
            self.validate_payload(payload)
            return Message.CHART, payload
        payload = {
            "report_id": str(uuid.uuid4()),
            "type": "budget",
            "generated_at": datetime.now().isoformat(),
            "source_refs": ["sample_data"],
            "chart_url": f"data:image/png;base64,{chart_data}",
            "summary_markdown": "## Monthly Expenses by Category\n\nThis chart shows your spending breakdown by category for the selected period.",
        }
        if "chart image" in lower:
            self.validate_payload(payload)
            return Message.IMAGE, payload
        self.validate_payload(payload)
        return Message.CHART, payload
    def _generate_sample_chart(self) -> str:
        """Generate a sample monthly expenses by category bar chart."""
        # Sample data - in production, this would come from actual financial data
        categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 
                     'Bills & Utilities', 'Healthcare', 'Travel', 'Other']
        amounts = [1200, 800, 600, 400, 900, 300, 500, 200]
        
        # Create beautiful bar chart using Plotly
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=amounts,
                marker_color=['#2E86C1', '#28B463', '#F39C12', '#E74C3C', 
                             '#8E44AD', '#17A2B8', '#FFC107', '#6C757D'],
                text=[f'${amount:,}' for amount in amounts],
                textposition='auto',
            )
        ])
        
        # Customize layout for professional appearance
        fig.update_layout(
            title={
                'text': 'Monthly Expenses by Category',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial, sans-serif'}
            },
            xaxis_title='Category',
            yaxis_title='Amount ($)',
            template='plotly_white',  # Clean, professional theme
            showlegend=False,
            height=500,
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(size=12, family='Arial, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        # Style the axes
        fig.update_xaxes(tickangle=45, title_font_size=14)
        fig.update_yaxes(title_font_size=14, tickformat='$,.0f')
        
        # Export to PNG and encode as base64
        img_bytes = fig.to_image(format="png", width=800, height=500, scale=2)
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return img_base64

    def _generate_net_worth_trend(self, data: List[Dict]) -> str:
        """Generate net worth trend chart (example for future implementation)."""
        # This would be implemented when we have actual net worth data
        pass
    
    def _generate_portfolio_allocation(self, holdings: List[Dict]) -> str:
        """Generate portfolio allocation pie chart (example for future implementation)."""
        # This would be implemented when we have actual portfolio data
        pass
    
    def _generate_debt_payoff_timeline(self, debts: List[Dict]) -> str:
        """Generate debt payoff timeline chart (example for future implementation)."""
        # This would be implemented when we have actual debt data
        pass
