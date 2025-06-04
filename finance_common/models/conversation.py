from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ..db import Base


class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    created_at = Column(DateTime)

    messages = relationship("Message", back_populates="conversation")

    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, user_id={self.user_id})"


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"))
    sender = Column(String(10))
    content_type = Column(String(20), default="text")
    payload = Column(JSON, default=dict)
    timestamp = Column(DateTime)
    status = Column(String(20), default="sent")

    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"Message(id={self.id}, conversation_id={self.conversation_id})"
