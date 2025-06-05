"""
ADK Chat Service for Agent Service.
Handles chat interactions and integrates with the OpenAPI-based finance tools.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from agents_adk.agent import create_all_agents
from agents_adk.state.conversation_state import ConversationState
from agents_adk.workflows.finance_workflows import (
    OnboardingWorkflow, 
    BudgetCreationWorkflow, 
    GoalTrackingWorkflow, 
    FinancialHealthCheckWorkflow
)
from tools.finance_data_client import get_finance_client

logger = logging.getLogger(__name__)

# Import ADK components for proper agent execution
try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    ADK_AVAILABLE = True
    logger.info("ADK framework is available")
except ImportError as e:
    logger.warning(f"ADK framework not available: {e}")
    ADK_AVAILABLE = False
    # Create stub classes for development
    class Runner:
        def __init__(self, *args, **kwargs): pass
    class InMemorySessionService:
        async def create_session(self, *args, **kwargs): return None
    class types:
        class Content:
            def __init__(self, *args, **kwargs): pass
        class Part:
            def __init__(self, *args, **kwargs): pass


class ADKChatService:
    """Service for handling ADK agent chat interactions with OpenAPI integration."""
    
    def __init__(self):
        """Initialize the ADK chat service."""
        self.agents = create_all_agents()
        
        # Initialize workflows directly
        self.workflows = {
            'onboarding': OnboardingWorkflow(),
            'budget_creation': BudgetCreationWorkflow(),
            'goal_tracking': GoalTrackingWorkflow(),
            'financial_health_check': FinancialHealthCheckWorkflow()
        }
        
        self.conversation_states = {}  # In-memory storage for conversation states
        self.adk_sessions = {}  # Persistent ADK session cache per user
        self.adk_runners = {}  # Persistent ADK runner cache per user
        
        # Initialize session service for ADK
        if ADK_AVAILABLE:
            self.session_service = InMemorySessionService()
        else:
            self.session_service = None
            
        logger.info("ADKChatService initialized with OpenAPI client integration and persistent session management")
    
    def _before_tool_callback(self, tool, args, tool_context):
        """
        Before tool callback to inject user token into tool context.
        This ensures all tools have access to the user authentication token.
        """
        # Get user token from the current execution context
        if hasattr(self, '_current_user_token'):
            tool_context.state['user_token'] = self._current_user_token
            tool_context.state['token'] = self._current_user_token  # Fallback key
            # Handle FunctionTool objects which don't have __name__
            tool_name = getattr(tool, '__name__', getattr(tool, 'name', getattr(tool, 'function_name', 'unknown_tool')))
            logger.debug(f"Injected user token into tool context for tool: {tool_name}")
        else:
            tool_name = getattr(tool, '__name__', getattr(tool, 'name', getattr(tool, 'function_name', 'unknown_tool')))
            logger.warning(f"No user token available for tool: {tool_name}")
    
    def get_conversation_state(self, user_token: str) -> ConversationState:
        """Get or create conversation state for user."""
        if user_token not in self.conversation_states:
            # Try to load conversation context from API
            try:
                client = get_finance_client()
                context = client.get_conversation_context_sync(token=user_token)
                
                # Initialize with context from API if available
                state = ConversationState(
                    user_id=user_token,
                    context=context.get('context', {})
                )
                self.conversation_states[user_token] = state
                logger.info(f"Loaded conversation state for user {user_token}")
                
            except Exception as e:
                if "401" in str(e) or "Unauthorized" in str(e):
                    logger.warning(f"Authentication failed when loading conversation context for user {user_token}: {e}")
                else:
                    logger.warning(f"Could not load conversation context from API for user {user_token}: {e}")
                # Create new state if loading fails
                state = ConversationState(user_id=user_token)
                self.conversation_states[user_token] = state
                
        return self.conversation_states[user_token]
    
    async def _get_or_create_adk_session(self, user_token: str) -> tuple:
        """Get or create persistent ADK session and runner for user."""
        if not ADK_AVAILABLE:
            return None, None
            
        # Use consistent session ID based on user token only
        session_id = f"session_{user_token}"
        
        # Check if we already have a session for this user
        if user_token in self.adk_sessions and user_token in self.adk_runners:
            logger.debug(f"Reusing existing ADK session for user {user_token}")
            return self.adk_sessions[user_token], self.adk_runners[user_token]
        
        try:
            # Create new session for this user
            session = await self.session_service.create_session(
                app_name="FinanceAgent", 
                user_id=user_token, 
                session_id=session_id
            )
            
            # Create runner for the session
            runner = Runner(
                agent=None,  # Will be set per agent call
                app_name="FinanceAgent", 
                session_service=self.session_service
            )
            
            # Cache the session and runner
            self.adk_sessions[user_token] = session
            self.adk_runners[user_token] = runner
            
            logger.info(f"Created new ADK session for user {user_token} with session_id: {session_id}")
            return session, runner
            
        except Exception as e:
            logger.error(f"Failed to create ADK session for user {user_token}: {e}")
            return None, None

    async def _run_adk_agent(self, agent, message: str, user_token: str, financial_context: Dict[str, Any]) -> str:
        """
        Run an ADK agent using proper Runner pattern with persistent sessions.
        
        Args:
            agent: ADK Agent object
            message: User message
            user_token: User authentication token 
            financial_context: Financial context for the agent
            
        Returns:
            Agent response text
        """
        if not ADK_AVAILABLE:
            return "ADK framework is not available. Please install google-adk package."
        
        try:
            # Store user token in instance for before_tool callback to access
            self._current_user_token = user_token
            
            # Get or create persistent session and runner
            session, runner = await self._get_or_create_adk_session(user_token)
            if not session or not runner:
                return "Failed to establish agent session. Please try again."
            
            # Use consistent session ID
            session_id = f"session_{user_token}"
            
            # Temporarily add our callback to the agent's existing callbacks
            original_callbacks = getattr(agent, 'before_tool_callback', [])
            if not isinstance(original_callbacks, list):
                original_callbacks = [original_callbacks] if original_callbacks else []
            
            # Add our callback to the list
            agent.before_tool_callback = original_callbacks + [self._before_tool_callback]
            
            try:
                # Update runner with current agent
                runner.agent = agent
                
                # Create properly formatted user message
                user_message = types.Content(
                    role='user', 
                    parts=[types.Part(text=message)]
                )
                
                # Run agent and collect response - process ALL events
                response_text = ""
                function_calls_made = 0
                function_responses_received = 0
                
                async for event in runner.run_async(
                    user_id=user_token,
                    session_id=session_id,
                    new_message=user_message
                ):
                    # Log ALL event types for debugging
                    logger.info(f"ADK Event: type={type(event).__name__}, is_final={event.is_final_response() if hasattr(event, 'is_final_response') else 'N/A'}")
                    
                    # Log event details for debugging
                    if hasattr(event, 'content') and event.content and event.content.parts:
                        logger.info(f"Event has {len(event.content.parts)} parts")
                        for i, part in enumerate(event.content.parts):
                            if hasattr(part, 'function_call') and part.function_call:
                                function_calls_made += 1
                                logger.info(f"🔧 Function call #{function_calls_made}: {part.function_call.name} with args: {part.function_call.args}")
                            elif hasattr(part, 'function_response') and part.function_response:
                                function_responses_received += 1
                                logger.info(f"📥 Function response #{function_responses_received} for: {part.function_response.name}: {part.function_response.response}")
                            elif hasattr(part, 'text') and part.text:
                                logger.info(f"💬 Text part #{i}: {part.text[:100]}...")
                            else:
                                logger.info(f"❓ Unknown part type #{i}: {type(part).__name__}")
                    else:
                        logger.info("Event has no content/parts")
                    
                    # Wait for final response that includes text
                    if event.is_final_response() and event.content and event.content.parts:
                        logger.info("Processing final response...")
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text = part.text
                                logger.info(f"Final text extracted: {response_text[:100]}...")
                                break
                        if response_text:
                            break
                
                logger.info(f"ADK agent {agent.name} made {function_calls_made} function calls, received {function_responses_received} responses, and generated response for user {user_token[:10]}...")
                return response_text or "Agent processed the request but didn't generate a response."
                
            finally:
                # Restore original callbacks
                agent.before_tool_callback = original_callbacks
            
        except Exception as e:
            logger.error(f"Error running ADK agent {agent.name}: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception details: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return f"I apologize, but I encountered an issue processing your request with the {agent.name} agent."
        finally:
            # Clean up the stored token
            if hasattr(self, '_current_user_token'):
                delattr(self, '_current_user_token')
    
    async def process_message(self, user_token: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user message and return agent response.
        
        Args:
            user_token: User authentication token (legacy, fallback)
            message: User message text
            context: Optional context dict (should contain 'user_token')
            
        Returns:
            Dictionary containing agent response and metadata
        """
        try:
            # Prioritize token from context for consistency with Django service
            actual_token = None
            if context and isinstance(context, dict):
                actual_token = context.get('user_token')
            if not actual_token:
                actual_token = user_token
            if not actual_token:
                logger.error("No valid user token provided in context or user_token argument.")
                return {
                    'content': 'Authentication error: No valid user token provided.',
                    'metadata': {'error': True, 'error_message': 'No valid user token provided.'}
                }
            
            # Log token usage for debugging
            if actual_token != user_token:
                logger.info(f"Using token from context: {actual_token[:10]}... (different from parameter: {user_token[:10] if user_token else 'None'}...)")
            else:
                logger.debug(f"Using consistent token: {actual_token[:10]}...")
            
            # Periodic session cleanup (every 100 messages to avoid overhead)
            import random
            if random.randint(1, 100) == 1:
                try:
                    self.cleanup_expired_sessions()
                except Exception as cleanup_error:
                    logger.warning(f"Session cleanup failed: {cleanup_error}")
            
            # Get conversation state using the actual token
            conversation_state = self.get_conversation_state(actual_token)
            
            # Add user message to conversation
            conversation_state.add_message("user", message)
            
            # Get financial context for the agent
            financial_context = {}
            try:
                client = get_finance_client()
                financial_context = client.get_financial_context_sync(
                    token=actual_token,
                    include_future_goals=True,
                    limit_transactions=50
                )
                
                # Update conversation state with fresh financial data
                conversation_state.update_context({
                    'financial_context': financial_context,
                    'last_context_update': 'current'
                })
                
                logger.debug(f"Successfully retrieved financial context for user {actual_token[:10]}...")
                
            except Exception as e:
                if "401" in str(e) or "Unauthorized" in str(e):
                    logger.warning(f"Authentication failed when fetching financial context for user {actual_token[:10]}...: {e}")
                    financial_context = {}
                    # Update context to indicate auth failure
                    conversation_state.update_context({
                        'financial_context_error': 'authentication_failed',
                        'last_context_update': 'failed'
                    })
                else:
                    logger.warning(f"Could not fetch financial context for user {actual_token[:10]}...: {e}")
                    financial_context = {}
            
            # Always start with orchestrator for proper routing
            agent_to_use = self.agents.get('orchestrator')
            agent_used = 'orchestrator'
            
            # Fallback to conversation agent if orchestrator not available
            if not agent_to_use:
                agent_to_use = self.agents.get('conversation_agent')
                agent_used = 'conversation'
            
            # Run the agent
            if agent_to_use:
                response_content = await self._run_adk_agent(
                    agent_to_use, message, actual_token, financial_context
                )
                
                # EMERGENCY FALLBACK: If response asks for parameters but user wants transactions, call tool directly  
                if (any(keyword in message.lower() for keyword in ['transaction', 'transactions']) and
                    ('date range' in response_content.lower() or 'category' in response_content.lower() or 'specify' in response_content.lower())):
                    logger.warning("Agent failed to call transaction tool - executing directly as fallback")
                    try:
                        from agents_adk.tools.finance_tools import get_user_transactions
                        from google.adk.tools.tool_context import ToolContext
                        
                        # Create mock tool context
                        mock_context = type('MockContext', (), {})()
                        mock_context.state = {'user_token': actual_token, 'token': actual_token}
                        
                        # Call tool directly
                        tool_result = get_user_transactions(
                            user_id="user",
                            date_range=None,
                            category=None, 
                            limit=10,
                            tool_context=mock_context
                        )
                        
                        # Parse result and create user-friendly response
                        import json
                        result_data = json.loads(tool_result)
                        if 'error' in result_data:
                            response_content = f"I encountered an error retrieving your transactions: {result_data['error']}"
                        elif 'transactions' in result_data:
                            transactions = result_data['transactions']
                            if transactions:
                                latest = transactions[0] if isinstance(transactions, list) and len(transactions) > 0 else transactions
                                if isinstance(latest, dict):
                                    response_content = f"Here is your most recent transaction:\n\n"
                                    response_content += f"**Date:** {latest.get('date', 'Unknown')}\n"
                                    response_content += f"**Amount:** ${abs(float(latest.get('amount', 0))):.2f}\n" 
                                    response_content += f"**Description:** {latest.get('description', 'Unknown')}\n"
                                    response_content += f"**Category:** {latest.get('category', 'Uncategorized')}\n"
                                    response_content += f"**Type:** {'Income' if latest.get('amount', 0) > 0 else 'Expense'}"
                                else:
                                    response_content = f"Found {len(transactions)} transactions. Here's the most recent one: {str(latest)}"
                            else:
                                response_content = "No transactions found."
                        
                        logger.info(f"Emergency fallback tool call successful for user {actual_token[:10]}...")
                        
                    except Exception as fallback_error:
                        logger.error(f"Emergency fallback also failed: {fallback_error}")
                        # Keep original response if fallback fails
                
            else:
                response_content = "I apologize, but the financial advisor is currently unavailable. Please try again later."
                agent_used = 'fallback'
            
            # Add agent response to conversation
            conversation_state.add_message("assistant", response_content)
            
            # Prepare response
            response = {
                'content': response_content,
                'metadata': {
                    'agent_type': 'financial_advisor',
                    'conversation_id': conversation_state.conversation_id,
                    'message_count': len(conversation_state.messages),
                    'financial_context_available': bool(financial_context),
                    'agent_used': agent_used,
                    'adk_available': ADK_AVAILABLE,
                    'session_persisted': actual_token in self.adk_sessions,
                    'token_source': 'context' if context and context.get('user_token') else 'parameter'
                }
            }
            
            logger.info(f"Processed message for user {actual_token[:10]}...: {len(message)} chars -> {len(response['content'])} chars, session_persisted: {actual_token in self.adk_sessions}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message for user {user_token}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                'content': 'I apologize, but I encountered a technical issue. Please try again.',
                'metadata': {
                    'error': True,
                    'error_message': str(e),
                    'agent_type': 'financial_advisor'
                }
            }
    
    async def send_message(self, user_id: str, text: str, context: Optional[Dict[str, Any]] = None) -> tuple[str, Dict[str, Any]]:
        """
        Send a message to the agent and get response (API compatibility method).
        
        Args:
            user_id: User identifier
            text: Message text
            context: Optional financial context
            
        Returns:
            Tuple of (content_type, payload)
        """
        try:
            # Process the message, always pass context
            response = await self.process_message(user_id, text, context)
            
            # Return in expected format for API
            return ("text", {
                "message": response.get('content', ''),
                "metadata": response.get('metadata', {}),
                "success": True
            })
            
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            return ("text", {
                "message": "I apologize, but I encountered an error processing your request.",
                "error": str(e),
                "success": False
            })
    
    def get_conversation_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user (sync version for API compatibility).
        
        Args:
            user_id: User identifier
            
        Returns:
            List of messages
        """
        try:
            conversation_state = self.get_conversation_state(user_id)
            return conversation_state.get_recent_messages()
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def clear_conversation_history(self, user_id: str) -> bool:
        """
        Clear conversation history for a user (sync version for API compatibility).
        
        Args:
            user_id: User identifier
            
        Returns:
            Success status
        """
        try:
            if user_id in self.conversation_states:
                del self.conversation_states[user_id]
            return True
        except Exception as e:
            logger.error(f"Error clearing conversation history: {e}")
            return False

    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """Clean up expired sessions to manage memory usage."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        expired_users = []
        
        for user_token, conversation_state in self.conversation_states.items():
            if conversation_state.last_updated < cutoff_time:
                expired_users.append(user_token)
        
        for user_token in expired_users:
            # Clean up conversation state
            if user_token in self.conversation_states:
                del self.conversation_states[user_token]
            
            # Clean up ADK sessions
            if user_token in self.adk_sessions:
                del self.adk_sessions[user_token]
            
            # Clean up ADK runners
            if user_token in self.adk_runners:
                del self.adk_runners[user_token]
            
            logger.info(f"Cleaned up expired session for user {user_token}")
        
        logger.info(f"Session cleanup complete: removed {len(expired_users)} expired sessions")


# Global service instance
_adk_chat_service = None


def get_adk_chat_service() -> ADKChatService:
    """Get the global ADK chat service instance."""
    global _adk_chat_service
    if _adk_chat_service is None:
        _adk_chat_service = ADKChatService()
    return _adk_chat_service


# Export singleton instance for direct import (FastAPI compatibility)
adk_chat_service = get_adk_chat_service() 