import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.transaction import Transaction
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    category: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    limit: Union[Unset, int] = 100,
    max_amount: Union[Unset, float] = UNSET,
    min_amount: Union[Unset, float] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["category"] = category

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["limit"] = limit

    params["max_amount"] = max_amount

    params["min_amount"] = min_amount

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/agent/transactions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Transaction"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Transaction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Transaction"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    limit: Union[Unset, int] = 100,
    max_amount: Union[Unset, float] = UNSET,
    min_amount: Union[Unset, float] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
) -> Response[list["Transaction"]]:
    """Get Filtered Transactions

     Retrieve transactions with filtering options for agent analysis.

    Args:
        category (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        limit (Union[Unset, int]):  Default: 100.
        max_amount (Union[Unset, float]):
        min_amount (Union[Unset, float]):
        start_date (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Transaction']]
    """

    kwargs = _get_kwargs(
        category=category,
        end_date=end_date,
        limit=limit,
        max_amount=max_amount,
        min_amount=min_amount,
        start_date=start_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    limit: Union[Unset, int] = 100,
    max_amount: Union[Unset, float] = UNSET,
    min_amount: Union[Unset, float] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
) -> Optional[list["Transaction"]]:
    """Get Filtered Transactions

     Retrieve transactions with filtering options for agent analysis.

    Args:
        category (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        limit (Union[Unset, int]):  Default: 100.
        max_amount (Union[Unset, float]):
        min_amount (Union[Unset, float]):
        start_date (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Transaction']
    """

    return sync_detailed(
        client=client,
        category=category,
        end_date=end_date,
        limit=limit,
        max_amount=max_amount,
        min_amount=min_amount,
        start_date=start_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    limit: Union[Unset, int] = 100,
    max_amount: Union[Unset, float] = UNSET,
    min_amount: Union[Unset, float] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
) -> Response[list["Transaction"]]:
    """Get Filtered Transactions

     Retrieve transactions with filtering options for agent analysis.

    Args:
        category (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        limit (Union[Unset, int]):  Default: 100.
        max_amount (Union[Unset, float]):
        min_amount (Union[Unset, float]):
        start_date (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Transaction']]
    """

    kwargs = _get_kwargs(
        category=category,
        end_date=end_date,
        limit=limit,
        max_amount=max_amount,
        min_amount=min_amount,
        start_date=start_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    limit: Union[Unset, int] = 100,
    max_amount: Union[Unset, float] = UNSET,
    min_amount: Union[Unset, float] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
) -> Optional[list["Transaction"]]:
    """Get Filtered Transactions

     Retrieve transactions with filtering options for agent analysis.

    Args:
        category (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        limit (Union[Unset, int]):  Default: 100.
        max_amount (Union[Unset, float]):
        min_amount (Union[Unset, float]):
        start_date (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Transaction']
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
            end_date=end_date,
            limit=limit,
            max_amount=max_amount,
            min_amount=min_amount,
            start_date=start_date,
        )
    ).parsed
