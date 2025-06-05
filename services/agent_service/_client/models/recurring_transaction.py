import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecurringTransaction")


@_attrs_define
class RecurringTransaction:
    """
    Attributes:
        id (int):
        name (str):
        date (datetime.date):
        value (float):
        user (Union[None, Unset, int]):
        credential (Union[None, Unset, int]):
    """

    id: int
    name: str
    date: datetime.date
    value: float
    user: Union[None, Unset, int] = UNSET
    credential: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        date = self.date.isoformat()

        value = self.value

        user: Union[None, Unset, int]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        credential: Union[None, Unset, int]
        if isinstance(self.credential, Unset):
            credential = UNSET
        else:
            credential = self.credential

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "date": date,
                "value": value,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        date = self.date.isoformat().encode()

        value = (None, str(self.value).encode(), "text/plain")

        user: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.user, Unset):
            user = UNSET
        elif isinstance(self.user, int):
            user = (None, str(self.user).encode(), "text/plain")
        else:
            user = (None, str(self.user).encode(), "text/plain")

        credential: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.credential, Unset):
            credential = UNSET
        elif isinstance(self.credential, int):
            credential = (None, str(self.credential).encode(), "text/plain")
        else:
            credential = (None, str(self.credential).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "name": name,
                "date": date,
                "value": value,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        date = isoparse(d.pop("date")).date()

        value = d.pop("value")

        def _parse_user(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_credential(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        credential = _parse_credential(d.pop("credential", UNSET))

        recurring_transaction = cls(
            id=id,
            name=name,
            date=date,
            value=value,
            user=user,
            credential=credential,
        )

        recurring_transaction.additional_properties = d
        return recurring_transaction

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
