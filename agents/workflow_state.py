from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    """Shared state for the LangGraph workflow."""

    user_input: str
    conversation: List[Dict[str, Any]] = field(default_factory=list)
    result: Dict[str, Any] = field(default_factory=dict)
    next_agent: Optional[str] = None
    done: bool = False
