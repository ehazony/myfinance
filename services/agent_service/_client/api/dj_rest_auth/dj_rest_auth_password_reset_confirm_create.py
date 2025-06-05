from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.password_reset_confirm import PasswordResetConfirm
from ...models.rest_auth_detail import RestAuthDetail
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        PasswordResetConfirm,
        PasswordResetConfirm,
        PasswordResetConfirm,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/dj-rest-auth/password/reset/confirm/",
    }

    if isinstance(body, PasswordResetConfirm):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PasswordResetConfirm):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PasswordResetConfirm):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RestAuthDetail]:
    if response.status_code == 200:
        response_200 = RestAuthDetail.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RestAuthDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        PasswordResetConfirm,
        PasswordResetConfirm,
        PasswordResetConfirm,
    ],
) -> Response[RestAuthDetail]:
    """Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.

    Args:
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RestAuthDetail]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union[
        PasswordResetConfirm,
        PasswordResetConfirm,
        PasswordResetConfirm,
    ],
) -> Optional[RestAuthDetail]:
    """Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.

    Args:
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RestAuthDetail
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        PasswordResetConfirm,
        PasswordResetConfirm,
        PasswordResetConfirm,
    ],
) -> Response[RestAuthDetail]:
    """Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.

    Args:
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RestAuthDetail]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        PasswordResetConfirm,
        PasswordResetConfirm,
        PasswordResetConfirm,
    ],
) -> Optional[RestAuthDetail]:
    """Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.

    Args:
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.
        body (PasswordResetConfirm): Serializer for confirming a password reset attempt.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RestAuthDetail
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
