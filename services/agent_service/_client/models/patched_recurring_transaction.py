import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRecurringTransaction")


@_attrs_define
class PatchedRecurringTransaction:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        date (Union[Unset, datetime.date]):
        value (Union[Unset, float]):
        user (Union[None, Unset, int]):
        credential (Union[None, Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    value: Union[Unset, float] = UNSET
    user: Union[None, Unset, int] = UNSET
    credential: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
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
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if date is not UNSET:
            field_dict["date"] = date
        if value is not UNSET:
            field_dict["value"] = value
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (
            self.id
            if isinstance(self.id, Unset)
            else (None, str(self.id).encode(), "text/plain")
        )

        name = (
            self.name
            if isinstance(self.name, Unset)
            else (None, str(self.name).encode(), "text/plain")
        )

        date: Union[Unset, bytes] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat().encode()

        value = (
            self.value
            if isinstance(self.value, Unset)
            else (None, str(self.value).encode(), "text/plain")
        )

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

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if date is not UNSET:
            field_dict["date"] = date
        if value is not UNSET:
            field_dict["value"] = value
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        value = d.pop("value", UNSET)

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

        patched_recurring_transaction = cls(
            id=id,
            name=name,
            date=date,
            value=value,
            user=user,
            credential=credential,
        )

        patched_recurring_transaction.additional_properties = d
        return patched_recurring_transaction

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
