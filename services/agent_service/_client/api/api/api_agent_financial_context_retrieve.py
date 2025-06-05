from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.financial_context import FinancialContext
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_future_goals: Union[Unset, bool] = True,
    limit_transactions: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_future_goals"] = include_future_goals

    params["limit_transactions"] = limit_transactions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/agent/financial-context/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[FinancialContext]:
    if response.status_code == 200:
        response_200 = FinancialContext.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[FinancialContext]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_future_goals: Union[Unset, bool] = True,
    limit_transactions: Union[Unset, int] = 100,
) -> Response[FinancialContext]:
    """Get Financial Context

     Retrieve complete financial context for agent processing including transactions, budgets, and goals.

    Args:
        include_future_goals (Union[Unset, bool]):  Default: True.
        limit_transactions (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FinancialContext]
    """

    kwargs = _get_kwargs(
        include_future_goals=include_future_goals,
        limit_transactions=limit_transactions,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    include_future_goals: Union[Unset, bool] = True,
    limit_transactions: Union[Unset, int] = 100,
) -> Optional[FinancialContext]:
    """Get Financial Context

     Retrieve complete financial context for agent processing including transactions, budgets, and goals.

    Args:
        include_future_goals (Union[Unset, bool]):  Default: True.
        limit_transactions (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FinancialContext
    """

    return sync_detailed(
        client=client,
        include_future_goals=include_future_goals,
        limit_transactions=limit_transactions,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_future_goals: Union[Unset, bool] = True,
    limit_transactions: Union[Unset, int] = 100,
) -> Response[FinancialContext]:
    """Get Financial Context

     Retrieve complete financial context for agent processing including transactions, budgets, and goals.

    Args:
        include_future_goals (Union[Unset, bool]):  Default: True.
        limit_transactions (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FinancialContext]
    """

    kwargs = _get_kwargs(
        include_future_goals=include_future_goals,
        limit_transactions=limit_transactions,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_future_goals: Union[Unset, bool] = True,
    limit_transactions: Union[Unset, int] = 100,
) -> Optional[FinancialContext]:
    """Get Financial Context

     Retrieve complete financial context for agent processing including transactions, budgets, and goals.

    Args:
        include_future_goals (Union[Unset, bool]):  Default: True.
        limit_transactions (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FinancialContext
    """

    return (
        await asyncio_detailed(
            client=client,
            include_future_goals=include_future_goals,
            limit_transactions=limit_transactions,
        )
    ).parsed
