from pydantic import BaseModel
from typing import Dict, Any, Optional

class ChatRequest(BaseModel):
    user_id: str
    text: str
    context: Optional[Dict[str, Any]] = None  # Financial context from core API

class ChatResponse(BaseModel):
    content_type: str
    payload: Dict[str, Any]

class Message(BaseModel):
    sender: str
    content_type: str
    payload: Dict[str, Any] 