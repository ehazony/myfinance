"""
Finance Data Client for Agent Service.
Provides a simplified interface to the Django Core API using auto-generated client.
"""

import json
import logging
import sys
import os
import inspect
from typing import Dict, Any, Optional, List, Union, get_origin, get_args
from dataclasses import dataclass
from datetime import datetime, date

# Add the current directory to sys.path to allow absolute imports
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from _client.client import Client, AuthenticatedClient
from _client.api.api import (
    api_agent_financial_context_retrieve,
    api_agent_transactions_list,
    api_agent_budget_analysis_list,
    api_agent_account_summary_list,
    api_agent_conversation_context_retrieve
)
from _client.models import (
    FinancialContext,
    Transaction,
    BudgetTarget,
    AccountSummary,
    ConversationContext
)
from _client.types import Response, UNSET
from _client.errors import UnexpectedStatus

logger = logging.getLogger(__name__)


class OpenAPIClientWrapper:
    """
    Wrapper for OpenAPI client that automatically converts None values to UNSET.
    This prevents errors when optional parameters are passed as None instead of UNSET.
    Uses type inspection to determine which parameters should auto-convert based on their type annotations.
    """
    
    def __init__(self, client):
        self._client = client
    
    def _should_convert_none_to_unset(self, method, param_name: str) -> bool:
        """
        Determine if a parameter should have None converted to UNSET based on its type annotation.
        Returns True if the parameter is typed as Union[Unset, SomeType] (None not allowed).
        Returns False if the parameter is typed as Union[Unset, None, SomeType] (None allowed).
        """
        try:
            signature = inspect.signature(method)
            if param_name not in signature.parameters:
                return False
            
            param = signature.parameters[param_name]
            annotation = param.annotation
            
            # Check if it's a Union type
            if get_origin(annotation) is Union:
                args = get_args(annotation)
                # If the Union includes UNSET but not None, convert None to UNSET
                # If the Union includes both UNSET and None, preserve None
                has_unset = any(getattr(arg, '__name__', None) == 'Unset' for arg in args)
                has_none = type(None) in args
                
                if has_unset and not has_none:
                    return True  # Convert None → UNSET
                else:
                    return False  # Preserve None
            
            return False  # Not a Union type, preserve as-is
            
        except Exception as e:
            logger.debug(f"Could not inspect parameter {param_name}: {e}")
            return False  # Conservative: preserve None on inspection failure
    
    def __getattr__(self, name):
        # Get the original method from the client
        original_method = getattr(self._client, name)
        
        # If it's not callable, return as-is (for properties, etc.)
        if not callable(original_method):
            return original_method
        
        # Return a wrapper function that processes kwargs
        def wrapper(*args, **kwargs):
            # Type-based conversion: inspect method signature to determine conversions
            processed_kwargs = {}
            for key, value in kwargs.items():
                if value is None and self._should_convert_none_to_unset(original_method, key):
                    # Convert to UNSET for parameters that don't accept None
                    processed_kwargs[key] = UNSET
                    logger.debug(f"Auto-converted None to UNSET for parameter '{key}' based on type annotation")
                else:
                    # Preserve None for parameters that explicitly allow it
                    processed_kwargs[key] = value
            
            # Call the original method with processed kwargs
            return original_method(*args, **processed_kwargs)
        
        return wrapper


class FinanceDataClient:
    """Client for accessing finance data using generated OpenAPI client."""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the finance data client.
        
        Args:
            base_url: Base URL of the Django Core API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self._client = None
        
    def _get_client(self, token: str) -> OpenAPIClientWrapper:
        """Get or create authenticated client instance wrapped for automatic UNSET handling."""
        if not self._client or getattr(self._client, 'token', None) != token:
            auth_client = AuthenticatedClient(
                base_url=self.base_url,
                token=token,
                prefix="Token",
                timeout=self.timeout
            )
            self._client = OpenAPIClientWrapper(auth_client)
        return self._client
    
    async def get_financial_context(
        self, 
        token: str, 
        include_future_goals: bool = True,
        limit_transactions: int = 100
    ) -> Dict[str, Any]:
        """
        Retrieve complete financial context for agent processing.
        
        Args:
            token: Authentication token
            include_future_goals: Include future financial goals
            limit_transactions: Limit number of recent transactions
            
        Returns:
            Dictionary containing financial context data
        """
        try:
            client = self._get_client(token)
            
            response: Response[FinancialContext] = await api_agent_financial_context_retrieve.asyncio_detailed(
                client=client,
                include_future_goals=include_future_goals,
                limit_transactions=limit_transactions
            )
            
            if response.status_code == 200:
                context = response.parsed
                return {
                    "transactions": [t.to_dict() for t in context.transactions] if context.transactions else [],
                    "category_mapping": context.category_mapping.to_dict() if context.category_mapping else {},
                    "budget_targets": context.budget_targets.to_dict() if context.budget_targets else {},
                    "budget_inputs": context.budget_inputs.to_dict() if context.budget_inputs else {},
                    "user_id": context.user_id if context.user_id else None,
                    "username": context.username if context.username else None
                }
            else:
                logger.error(f"Failed to fetch financial context: {response.status_code}")
                return {}
                
        except UnexpectedStatus as e:
            logger.error(f"Unexpected status getting financial context: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting financial context: {e}")
            return {}
    
    async def get_filtered_transactions(
        self,
        token: str,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve transactions with filtering options.
        
        Args:
            token: Authentication token
            category: Filter by transaction category
            start_date: Start date filter (datetime.date)
            end_date: End date filter (datetime.date)
            min_amount: Minimum amount filter
            max_amount: Maximum amount filter
            limit: Maximum number of transactions to return
            
        Returns:
            List of transaction dictionaries
        """
        logger.info(
            f"Async get_filtered_transactions called with: category='{category}', "
            f"start_date='{start_date}', end_date='{end_date}', limit={limit}, "
            f"min_amount={min_amount}, max_amount={max_amount}, token=HIDDEN"
        )
        try:
            client = self._get_client(token)
            
            response: Response[List[Transaction]] = await api_agent_transactions_list.asyncio_detailed(
                client=client,
                category=category,
                start_date=start_date,
                end_date=end_date,
                min_amount=min_amount,
                max_amount=max_amount,
                limit=limit
            )
            
            if response.status_code == 200:
                transactions = response.parsed or []
                logger.debug(f"Async get_filtered_transactions raw response (first 2 if many): {transactions[:2]}")
                return [t.to_dict() for t in transactions]
            else:
                logger.error(f"Failed to fetch transactions: {response.status_code}, content: {response.content!r}")
                return []
                
        except UnexpectedStatus as e:
            logger.error(f"Unexpected status getting transactions: {e}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Error getting transactions: {e}", exc_info=True)
            return []
    
    async def get_budget_analysis(
        self,
        token: str,
        period: str = "current_month"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve budget vs actual spending analysis.
        
        Args:
            token: Authentication token
            period: Analysis period ('current_month', 'last_month', 'ytd')
            
        Returns:
            List of budget target dictionaries
        """
        try:
            client = self._get_client(token)
            
            response: Response[List[BudgetTarget]] = await api_agent_budget_analysis_list.asyncio_detailed(
                client=client,
                period=period
            )
            
            if response.status_code == 200:
                budget_targets = response.parsed or []
                return [bt.to_dict() for bt in budget_targets]
            else:
                logger.error(f"Failed to fetch budget analysis: {response.status_code}")
                return []
                
        except UnexpectedStatus as e:
            logger.error(f"Unexpected status getting budget analysis: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting budget analysis: {e}")
            return []
    
    async def get_account_summary(self, token: str) -> List[Dict[str, Any]]:
        """
        Retrieve account balances and transaction counts.
        
        Args:
            token: Authentication token
            
        Returns:
            List of account summary dictionaries
        """
        try:
            client = self._get_client(token)
            
            response: Response[List[AccountSummary]] = await api_agent_account_summary_list.asyncio_detailed(
                client=client
            )
            
            if response.status_code == 200:
                summaries = response.parsed or []
                return [s.to_dict() for s in summaries]
            else:
                logger.error(f"Failed to fetch account summary: {response.status_code}")
                return []
                
        except UnexpectedStatus as e:
            logger.error(f"Unexpected status getting account summary: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting account summary: {e}")
            return []
    
    async def get_conversation_context(self, token: str) -> Dict[str, Any]:
        """
        Retrieve conversation history and context for agent memory.
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary containing conversation context
        """
        try:
            client = self._get_client(token)
            
            response: Response[ConversationContext] = await api_agent_conversation_context_retrieve.asyncio_detailed(
                client=client
            )
            
            if response.status_code == 200:
                context = response.parsed
                return {
                    "recent_messages": [m.to_dict() for m in context.recent_messages] if context.recent_messages else [],
                    "conversation_id": context.conversation_id,
                    "message_count": context.message_count,
                    "last_activity": context.last_activity.isoformat() if context.last_activity else None,
                    "recent_topics": context.recent_topics if context.recent_topics else []
                }
            else:
                logger.error(f"Failed to fetch conversation context: {response.status_code}")
                return {}
                
        except UnexpectedStatus as e:
            logger.error(f"Unexpected status getting conversation context: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return {}


# Synchronous wrappers for backward compatibility
class SyncFinanceDataClient(FinanceDataClient):
    """Synchronous wrapper for FinanceDataClient."""
    
    def _run_async(self, coro):
        """Run async coroutine in a thread to avoid event loop conflicts."""
        import asyncio
        import threading
        import concurrent.futures
        import logging
        
        logger = logging.getLogger(__name__)
        
        def run_in_new_thread():
            """Create a new event loop in a separate thread."""
            try:
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(coro)
                    logger.debug("Successfully completed async operation in new thread")
                    return result
                finally:
                    # Properly close the loop
                    try:
                        # Cancel any remaining tasks
                        pending = asyncio.all_tasks(loop)
                        for task in pending:
                            task.cancel()
                        
                        # Wait for cancelled tasks to complete
                        if pending:
                            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    except Exception as cleanup_error:
                        logger.warning(f"Error during event loop cleanup: {cleanup_error}")
                    finally:
                        loop.close()
            except Exception as thread_error:
                logger.error(f"Error in async thread execution: {thread_error}", exc_info=True)
                raise
        
        try:
            # Check if we're already in an event loop
            try:
                current_loop = asyncio.get_running_loop()
                logger.debug("Running loop detected, using thread executor")
                
                # If we have a running loop, use a thread executor
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(run_in_new_thread)
                    try:
                        result = future.result(timeout=30)  # 30 second timeout
                        return result
                    except concurrent.futures.TimeoutError:
                        logger.error("Async operation timed out after 30 seconds")
                        raise
                        
            except RuntimeError:
                # No running loop, safe to use asyncio.run
                logger.debug("No running loop detected, using asyncio.run")
                try:
                    return asyncio.run(coro)
                except RuntimeError as e:
                    if "Event loop is closed" in str(e) or "cannot be called from a running event loop" in str(e):
                        logger.warning(f"Event loop issue, falling back to thread: {e}")
                        # Fallback to thread execution
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(run_in_new_thread)
                            return future.result(timeout=30)
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Failed to execute async operation: {e}", exc_info=True)
            # Last resort: try direct execution
            try:
                return run_in_new_thread()
            except Exception as final_error:
                logger.error(f"All async execution methods failed: {final_error}", exc_info=True)
                raise final_error
    
    def get_financial_context_sync(self, token: str, **kwargs) -> Dict[str, Any]:
        """Synchronous wrapper for get_financial_context."""
        logger.info(f"Sync get_financial_context_sync called with: token=HIDDEN, kwargs={kwargs}")
        try:
            return self._run_async(self.get_financial_context(token, **kwargs))
        except Exception as e:
            logger.error(f"Error getting financial context synchronously: {e}", exc_info=True)
            return {}
    
    def get_conversation_context_sync(self, token: str) -> Dict[str, Any]:
        """Synchronous wrapper for get_conversation_context."""
        logger.info(f"Sync get_conversation_context_sync called with: token=HIDDEN")
        try:
            return self._run_async(self.get_conversation_context(token))
        except Exception as e:
            if "401" in str(e) or "Unauthorized" in str(e):
                logger.warning(f"Authentication failed when getting conversation context synchronously: {e}", exc_info=True)
            else:
                logger.error(f"Error getting conversation context synchronously: {e}", exc_info=True)
            return {}
    
    def get_filtered_transactions_sync(self, token: str, **kwargs) -> List[Dict[str, Any]]:
        """Synchronous wrapper for get_filtered_transactions."""
        logger.info(f"Sync get_filtered_transactions_sync called with: token=HIDDEN, kwargs={kwargs}")
        try:
            return self._run_async(self.get_filtered_transactions(token, **kwargs))
        except Exception as e:
            logger.error(f"Error getting filtered transactions synchronously: {e}", exc_info=True)
            return []
    
    def get_budget_analysis_sync(self, token: str, **kwargs) -> List[Dict[str, Any]]:
        """Synchronous wrapper for get_budget_analysis."""
        logger.info(f"Sync get_budget_analysis_sync called with: token=HIDDEN, kwargs={kwargs}")
        try:
            return self._run_async(self.get_budget_analysis(token, **kwargs))
        except Exception as e:
            logger.error(f"Error getting budget analysis synchronously: {e}", exc_info=True)
            return []
    
    def get_account_summary_sync(self, token: str) -> List[Dict[str, Any]]:
        """Synchronous wrapper for get_account_summary."""
        logger.info(f"Sync get_account_summary_sync called with: token=HIDDEN")
        try:
            return self._run_async(self.get_account_summary(token))
        except Exception as e:
            logger.error(f"Error getting account summary synchronously: {e}", exc_info=True)
            return []


# Global client instance
_finance_client = SyncFinanceDataClient()


def get_finance_client() -> SyncFinanceDataClient:
    """Get the global finance client instance."""
    return _finance_client 