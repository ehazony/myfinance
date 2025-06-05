import logging
from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse, Message
from services.adk_chat_service import adk_chat_service
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/send", response_model=ChatResponse)
async def send_chat(request: ChatRequest):
    """Process a chat message using the ADK chat service."""
    try:
        logger.info(f"Processing chat request for user {request.user_id}: {request.text}")
        if request.context:
            logger.info(f"Financial context provided: {len(request.context.get('transactions', []))} transactions")
        
        # Process with ADK chat service
        content_type, payload = await adk_chat_service.send_message(
            request.user_id, 
            request.text,
            request.context  # Pass the financial context
        )
        
        return ChatResponse(content_type=content_type, payload=payload)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")

@router.get("/history", response_model=List[Message])
def chat_history(user_id: str):
    """Get conversation history for a user."""
    try:
        messages = adk_chat_service.get_conversation_history(user_id)
        logger.info(f"Retrieved {len(messages)} messages for user {user_id}")
        return messages
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@router.delete("/history/{user_id}")
def clear_chat_history(user_id: str):
    """Clear conversation history for a user."""
    try:
        success = adk_chat_service.clear_conversation_history(user_id)
        if success:
            return {"message": f"Chat history cleared for user {user_id}"}
        else:
            return {"message": f"No chat history found for user {user_id}"}
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

@router.delete("/sessions/{user_id}")
def clear_user_sessions(user_id: str):
    """Clear ADK sessions and conversation states for a user."""
    try:
        # Clear from ADK chat service
        if hasattr(adk_chat_service, 'conversation_states') and user_id in adk_chat_service.conversation_states:
            del adk_chat_service.conversation_states[user_id]
        
        if hasattr(adk_chat_service, 'adk_sessions') and user_id in adk_chat_service.adk_sessions:
            del adk_chat_service.adk_sessions[user_id]
        
        if hasattr(adk_chat_service, 'adk_runners') and user_id in adk_chat_service.adk_runners:
            del adk_chat_service.adk_runners[user_id]
        
        return {"message": f"All sessions cleared for user {user_id}"}
    except Exception as e:
        logger.error(f"Error clearing sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear sessions")

@router.delete("/sessions/all")
def clear_all_sessions():
    """Clear all ADK sessions and conversation states for debugging."""
    try:
        cleared_count = 0
        
        # Clear conversation states
        if hasattr(adk_chat_service, 'conversation_states'):
            cleared_count += len(adk_chat_service.conversation_states)
            adk_chat_service.conversation_states.clear()
        
        # Clear ADK sessions
        if hasattr(adk_chat_service, 'adk_sessions'):
            adk_chat_service.adk_sessions.clear()
        
        # Clear ADK runners
        if hasattr(adk_chat_service, 'adk_runners'):
            adk_chat_service.adk_runners.clear()
        
        return {"message": f"All sessions cleared ({cleared_count} conversation states)"}
    except Exception as e:
        logger.error(f"Error clearing all sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear all sessions") 