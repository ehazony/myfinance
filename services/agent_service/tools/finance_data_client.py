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

    def _get_client(self, token: str) -> AuthenticatedClient:
        """Get or create authenticated client instance."""
        if not self._client or getattr(self._client, 'token', None) != token:
            self._client = AuthenticatedClient(
                base_url=self.base_url,
                token=token,
                prefix="Token",
                timeout=self.timeout
            )
        return self._client

    def _sanitize_kwargs(self, func, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ``None`` values to ``UNSET`` and handle type conversions for the OpenAPI client."""
        from datetime import datetime, date
        import re
        
        sanitized = {}
        try:
            signature = inspect.signature(func)
        except Exception:
            return kwargs

        for name, value in kwargs.items():
            # Handle None values
            if value is None and name in signature.parameters:
                param = signature.parameters[name]
                annotation = param.annotation
                if get_origin(annotation) is Union:
                    args = get_args(annotation)
                    has_unset = any(getattr(a, '__name__', None) == 'Unset' for a in args)
                    has_none = type(None) in args
                    if has_unset and not has_none:
                        sanitized[name] = UNSET
                        continue
            
            # Handle date string conversion for parameters typed as date
            if value is not None and isinstance(value, str) and name in signature.parameters:
                param = signature.parameters[name]
                annotation = param.annotation
                
                # Check if this parameter is typed to accept date objects
                is_date_param = False
                if get_origin(annotation) is Union:
                    args = get_args(annotation)
                    is_date_param = any(arg == date for arg in args)
                elif annotation == date:
                    is_date_param = True
                
                if is_date_param:
                    try:
                        # Try to parse common date formats
                        if re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                            # ISO format: YYYY-MM-DD
                            sanitized[name] = datetime.strptime(value, '%Y-%m-%d').date()
                            logger.debug(f"Converted string '{value}' to date object for parameter '{name}' based on type annotation")
                            continue
                        elif re.match(r'^\d{4}-\d{2}-\d{2}T', value):
                            # ISO datetime format
                            sanitized[name] = datetime.fromisoformat(value.replace('Z', '+00:00')).date()
                            logger.debug(f"Converted datetime string '{value}' to date object for parameter '{name}' based on type annotation")
                            continue
                        else:
                            # If it's not a recognizable date format, set to UNSET to avoid errors
                            logger.warning(f"Could not parse date string '{value}' for parameter '{name}' (typed as date), setting to UNSET")
                            sanitized[name] = UNSET
                            continue
                    except Exception as e:
                        logger.warning(f"Failed to convert date string '{value}' for parameter '{name}' (typed as date): {e}, setting to UNSET")
                        sanitized[name] = UNSET
                        continue
            
            sanitized[name] = value
        return sanitized

    async def _async_api_call(self, func, **kwargs):
        """Helper to call async OpenAPI functions with sanitized ``kwargs``."""
        sanitized = self._sanitize_kwargs(func, kwargs)
        return await func(**sanitized)
    
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
            
            response: Response[FinancialContext] = await self._async_api_call(
                api_agent_financial_context_retrieve.asyncio_detailed,
                client=client,
                include_future_goals=include_future_goals,
                limit_transactions=limit_transactions,
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
            
            response: Response[List[Transaction]] = await self._async_api_call(
                api_agent_transactions_list.asyncio_detailed,
                client=client,
                category=category,
                start_date=start_date,
                end_date=end_date,
                min_amount=min_amount,
                max_amount=max_amount,
                limit=limit,
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
            
            response: Response[List[BudgetTarget]] = await self._async_api_call(
                api_agent_budget_analysis_list.asyncio_detailed,
                client=client,
                period=period,
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
            
            response: Response[List[AccountSummary]] = await self._async_api_call(
                api_agent_account_summary_list.asyncio_detailed,
                client=client,
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
            
            response: Response[ConversationContext] = await self._async_api_call(
                api_agent_conversation_context_retrieve.asyncio_detailed,
                client=client,
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
        """Run async coroutine, handling event loop properly."""
        import asyncio
        import threading
        import concurrent.futures
        import logging
        
        logger = logging.getLogger(__name__)
        
        def run_in_new_thread():
            """Create a new event loop in a separate thread."""
            try:
                # Ensure we have a clean thread-local event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(coro)
                    logger.debug("Successfully completed async operation in new thread")
                    return result
                finally:
                    # Clean shutdown
                    try:
                        # Cancel all pending tasks
                        pending = asyncio.all_tasks(loop)
                        if pending:
                            for task in pending:
                                task.cancel()
                            # Wait for cancellation to complete
                            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    except Exception as cleanup_error:
                        logger.warning(f"Error during task cleanup: {cleanup_error}")
                    finally:
                        try:
                            loop.close()
                        except Exception as close_error:
                            logger.warning(f"Error closing loop: {close_error}")
                        finally:
                            asyncio.set_event_loop(None)
            except Exception as thread_error:
                logger.error(f"Error in async thread execution: {thread_error}", exc_info=True)
                raise
        
        try:
            # Check if we're already in an event loop
            try:
                current_loop = asyncio.get_running_loop()
                if current_loop and not current_loop.is_closed():
                    logger.debug("Running loop detected, using thread executor")
                    
                    # Always use thread executor when there's a running loop
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="FinanceClient") as executor:
                        future = executor.submit(run_in_new_thread)
                        try:
                            result = future.result(timeout=60)  # Increased timeout
                            return result
                        except concurrent.futures.TimeoutError:
                            logger.error("Async operation timed out after 60 seconds")
                            raise RuntimeError("Finance client operation timed out")
                else:
                    # Loop exists but is closed, use thread
                    logger.debug("Closed loop detected, using thread executor")
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="FinanceClient") as executor:
                        future = executor.submit(run_in_new_thread)
                        return future.result(timeout=60)
                        
            except RuntimeError:
                # No running loop, safe to use asyncio.run
                logger.debug("No running loop detected, using asyncio.run")
                try:
                    return asyncio.run(coro)
                except Exception as e:
                    logger.warning(f"asyncio.run failed: {e}, falling back to thread")
                    # Fallback to thread execution
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="FinanceClient") as executor:
                        future = executor.submit(run_in_new_thread)
                        return future.result(timeout=60)
                        
        except Exception as e:
            logger.error(f"Failed to execute async operation: {e}", exc_info=True)
            # Last resort: try direct execution in thread
            try:
                logger.debug("All methods failed, trying last resort thread execution")
                with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="FinanceClientLastResort") as executor:
                    future = executor.submit(run_in_new_thread)
                    return future.result(timeout=60)
            except Exception as final_error:
                logger.error(f"All async execution methods failed: {final_error}", exc_info=True)
                raise RuntimeError(f"Failed to execute async operation: {final_error}") from final_error
    
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