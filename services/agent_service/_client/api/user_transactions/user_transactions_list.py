import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.transaction_rest import TransactionRest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    date: Union[Unset, datetime.date] = UNSET,
    date_gt: Union[Unset, datetime.date] = UNSET,
    date_gte: Union[Unset, datetime.date] = UNSET,
    date_lt: Union[Unset, datetime.date] = UNSET,
    date_lte: Union[Unset, datetime.date] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_date: Union[Unset, str] = UNSET
    if not isinstance(date, Unset):
        json_date = date.isoformat()
    params["date"] = json_date

    json_date_gt: Union[Unset, str] = UNSET
    if not isinstance(date_gt, Unset):
        json_date_gt = date_gt.isoformat()
    params["date__gt"] = json_date_gt

    json_date_gte: Union[Unset, str] = UNSET
    if not isinstance(date_gte, Unset):
        json_date_gte = date_gte.isoformat()
    params["date__gte"] = json_date_gte

    json_date_lt: Union[Unset, str] = UNSET
    if not isinstance(date_lt, Unset):
        json_date_lt = date_lt.isoformat()
    params["date__lt"] = json_date_lt

    json_date_lte: Union[Unset, str] = UNSET
    if not isinstance(date_lte, Unset):
        json_date_lte = date_lte.isoformat()
    params["date__lte"] = json_date_lte

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user_transactions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["TransactionRest"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TransactionRest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["TransactionRest"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    date: Union[Unset, datetime.date] = UNSET,
    date_gt: Union[Unset, datetime.date] = UNSET,
    date_gte: Union[Unset, datetime.date] = UNSET,
    date_lt: Union[Unset, datetime.date] = UNSET,
    date_lte: Union[Unset, datetime.date] = UNSET,
) -> Response[list["TransactionRest"]]:
    """
    Args:
        date (Union[Unset, datetime.date]):
        date_gt (Union[Unset, datetime.date]):
        date_gte (Union[Unset, datetime.date]):
        date_lt (Union[Unset, datetime.date]):
        date_lte (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['TransactionRest']]
    """

    kwargs = _get_kwargs(
        date=date,
        date_gt=date_gt,
        date_gte=date_gte,
        date_lt=date_lt,
        date_lte=date_lte,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    date: Union[Unset, datetime.date] = UNSET,
    date_gt: Union[Unset, datetime.date] = UNSET,
    date_gte: Union[Unset, datetime.date] = UNSET,
    date_lt: Union[Unset, datetime.date] = UNSET,
    date_lte: Union[Unset, datetime.date] = UNSET,
) -> Optional[list["TransactionRest"]]:
    """
    Args:
        date (Union[Unset, datetime.date]):
        date_gt (Union[Unset, datetime.date]):
        date_gte (Union[Unset, datetime.date]):
        date_lt (Union[Unset, datetime.date]):
        date_lte (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['TransactionRest']
    """

    return sync_detailed(
        client=client,
        date=date,
        date_gt=date_gt,
        date_gte=date_gte,
        date_lt=date_lt,
        date_lte=date_lte,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    date: Union[Unset, datetime.date] = UNSET,
    date_gt: Union[Unset, datetime.date] = UNSET,
    date_gte: Union[Unset, datetime.date] = UNSET,
    date_lt: Union[Unset, datetime.date] = UNSET,
    date_lte: Union[Unset, datetime.date] = UNSET,
) -> Response[list["TransactionRest"]]:
    """
    Args:
        date (Union[Unset, datetime.date]):
        date_gt (Union[Unset, datetime.date]):
        date_gte (Union[Unset, datetime.date]):
        date_lt (Union[Unset, datetime.date]):
        date_lte (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['TransactionRest']]
    """

    kwargs = _get_kwargs(
        date=date,
        date_gt=date_gt,
        date_gte=date_gte,
        date_lt=date_lt,
        date_lte=date_lte,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    date: Union[Unset, datetime.date] = UNSET,
    date_gt: Union[Unset, datetime.date] = UNSET,
    date_gte: Union[Unset, datetime.date] = UNSET,
    date_lt: Union[Unset, datetime.date] = UNSET,
    date_lte: Union[Unset, datetime.date] = UNSET,
) -> Optional[list["TransactionRest"]]:
    """
    Args:
        date (Union[Unset, datetime.date]):
        date_gt (Union[Unset, datetime.date]):
        date_gte (Union[Unset, datetime.date]):
        date_lt (Union[Unset, datetime.date]):
        date_lte (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['TransactionRest']
    """

    return (
        await asyncio_detailed(
            client=client,
            date=date,
            date_gt=date_gt,
            date_gte=date_gte,
            date_lt=date_lt,
            date_lte=date_lte,
        )
    ).parsed
