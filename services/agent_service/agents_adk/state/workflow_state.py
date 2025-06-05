"""
ADK-based state management for the finance agent system.
Uses ADK's built-in session and memory capabilities.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


@dataclass
class FinanceSession:
    """Finance-specific session state that extends ADK session capabilities."""
    
    user_id: str
    session_id: str
    started_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    
    # Financial context
    current_financial_focus: Optional[str] = None  # budgeting, investing, etc.
    active_goals: List[Dict[str, Any]] = field(default_factory=list)
    recent_transactions_context: List[Dict[str, Any]] = field(default_factory=list)
    
    # Conversation flow
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    pending_actions: List[Dict[str, Any]] = field(default_factory=list)
    completed_workflows: List[str] = field(default_factory=list)
    
    # Agent coordination
    active_agent: Optional[str] = None
    agent_handoff_context: Dict[str, Any] = field(default_factory=dict)
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def add_conversation_entry(self, role: str, content: str, agent_name: str = None):
        """Add entry to conversation history."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'role': role,
            'content': content,
            'agent': agent_name,
        })
        self.update_activity()
    
    def set_financial_focus(self, focus: str):
        """Set current financial focus area."""
        self.current_financial_focus = focus
        self.update_activity()
    
    def add_pending_action(self, action_type: str, details: Dict[str, Any]):
        """Add a pending action that needs user confirmation."""
        self.pending_actions.append({
            'id': len(self.pending_actions),
            'type': action_type,
            'details': details,
            'created_at': datetime.now().isoformat()
        })
        self.update_activity()
    
    def complete_action(self, action_id: int):
        """Mark an action as completed."""
        self.pending_actions = [a for a in self.pending_actions if a['id'] != action_id]
        self.update_activity()


@dataclass
class WorkflowState:
    """Workflow state for multi-agent coordination."""
    
    session: FinanceSession
    current_step: str = "initial"
    workflow_type: str = "general"  # onboarding, budgeting, investing, etc.
    
    # Workflow data
    collected_data: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, bool] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    # Agent coordination
    next_agent: Optional[str] = None
    agent_results: Dict[str, Any] = field(default_factory=dict)
    completed_agents: List[str] = field(default_factory=list)
    
    # Control flow
    is_complete: bool = False
    requires_user_input: bool = False
    user_input_prompt: Optional[str] = None
    
    def advance_to_step(self, step: str, next_agent: str = None):
        """Advance workflow to next step."""
        self.current_step = step
        self.next_agent = next_agent
        self.session.update_activity()
    
    def add_agent_result(self, agent_name: str, result: Any):
        """Add result from an agent."""
        self.agent_results[agent_name] = result
        self.completed_agents.append(agent_name)
        self.session.update_activity()
    
    def add_error(self, error: str):
        """Add error to workflow state."""
        self.errors.append(error)
        self.session.update_activity()
    
    def require_user_input(self, prompt: str):
        """Mark that user input is required."""
        self.requires_user_input = True
        self.user_input_prompt = prompt
        self.session.update_activity()
    
    def complete_workflow(self):
        """Mark workflow as complete."""
        self.is_complete = True
        self.session.completed_workflows.append(self.workflow_type)
        self.session.update_activity() 