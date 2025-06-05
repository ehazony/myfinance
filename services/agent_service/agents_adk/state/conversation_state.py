"""
Conversation state management for ADK agents.
Handles conversation history and context in the OpenAPI-first architecture.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class ConversationState:
    """Manages conversation state and context for agent interactions."""
    
    def __init__(self, user_id: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize conversation state.
        
        Args:
            user_id: User identifier/token
            context: Initial context dictionary
        """
        self.user_id = user_id
        self.conversation_id = str(uuid.uuid4())
        self.context = context or {}
        self.messages: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Message role ('user', 'assistant', 'system')
            content: Message content
            metadata: Optional metadata for the message
        """
        message = {
            'id': str(uuid.uuid4()),
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.messages.append(message)
        self.last_updated = datetime.now()
    
    def get_recent_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent messages from conversation history.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of recent messages
        """
        return self.messages[-limit:] if limit > 0 else self.messages
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        Update conversation context with new data.
        
        Args:
            new_context: Dictionary of context updates
        """
        self.context.update(new_context)
        self.last_updated = datetime.now()
    
    def get_context(self, key: Optional[str] = None) -> Any:
        """
        Get context data.
        
        Args:
            key: Specific context key to retrieve, or None for all context
            
        Returns:
            Context value or entire context dictionary
        """
        if key is None:
            return self.context
        return self.context.get(key)
    
    def clear_messages(self) -> None:
        """Clear all messages from conversation history."""
        self.messages = []
        self.last_updated = datetime.now()
    
    def clear_context(self) -> None:
        """Clear all context data."""
        self.context = {}
        self.last_updated = datetime.now()
    
    def get_message_count(self) -> int:
        """Get total number of messages in conversation."""
        return len(self.messages)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversation state.
        
        Returns:
            Dictionary containing conversation metadata
        """
        return {
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'message_count': len(self.messages),
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'context_keys': list(self.context.keys())
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize conversation state to dictionary.
        
        Returns:
            Dictionary representation of conversation state
        """
        return {
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'context': self.context,
            'messages': self.messages,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationState':
        """
        Create ConversationState from dictionary.
        
        Args:
            data: Dictionary representation of conversation state
            
        Returns:
            ConversationState instance
        """
        state = cls(
            user_id=data['user_id'],
            context=data.get('context', {})
        )
        
        state.conversation_id = data.get('conversation_id', state.conversation_id)
        state.messages = data.get('messages', [])
        
        # Parse timestamps if provided
        if 'created_at' in data:
            try:
                state.created_at = datetime.fromisoformat(data['created_at'])
            except ValueError:
                pass
                
        if 'last_updated' in data:
            try:
                state.last_updated = datetime.fromisoformat(data['last_updated'])
            except ValueError:
                pass
        
        return state
    
    def __repr__(self) -> str:
        """String representation of conversation state."""
        return f"ConversationState(user_id='{self.user_id}', messages={len(self.messages)}, conversation_id='{self.conversation_id}')" 