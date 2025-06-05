import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransactionRest")


@_attrs_define
class TransactionRest:
    """
    Attributes:
        id (int):
        tag_name (str):
        date (datetime.date):
        name (str):
        value (float):
        month (Union[None, Unset, int]):
        month_date (Union[None, Unset, datetime.date]):
        bank (Union[Unset, bool]):
        identifier (Union[None, Unset, str]):
        user (Union[None, Unset, int]):
        credential (Union[None, Unset, int]):
        tag (Union[None, Unset, int]):
    """

    id: int
    tag_name: str
    date: datetime.date
    name: str
    value: float
    month: Union[None, Unset, int] = UNSET
    month_date: Union[None, Unset, datetime.date] = UNSET
    bank: Union[Unset, bool] = UNSET
    identifier: Union[None, Unset, str] = UNSET
    user: Union[None, Unset, int] = UNSET
    credential: Union[None, Unset, int] = UNSET
    tag: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tag_name = self.tag_name

        date = self.date.isoformat()

        name = self.name

        value = self.value

        month: Union[None, Unset, int]
        if isinstance(self.month, Unset):
            month = UNSET
        else:
            month = self.month

        month_date: Union[None, Unset, str]
        if isinstance(self.month_date, Unset):
            month_date = UNSET
        elif isinstance(self.month_date, datetime.date):
            month_date = self.month_date.isoformat()
        else:
            month_date = self.month_date

        bank = self.bank

        identifier: Union[None, Unset, str]
        if isinstance(self.identifier, Unset):
            identifier = UNSET
        else:
            identifier = self.identifier

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

        tag: Union[None, Unset, int]
        if isinstance(self.tag, Unset):
            tag = UNSET
        else:
            tag = self.tag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tag_name": tag_name,
                "date": date,
                "name": name,
                "value": value,
            }
        )
        if month is not UNSET:
            field_dict["month"] = month
        if month_date is not UNSET:
            field_dict["month_date"] = month_date
        if bank is not UNSET:
            field_dict["bank"] = bank
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        tag_name = (None, str(self.tag_name).encode(), "text/plain")

        date = self.date.isoformat().encode()

        name = (None, str(self.name).encode(), "text/plain")

        value = (None, str(self.value).encode(), "text/plain")

        month: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.month, Unset):
            month = UNSET
        elif isinstance(self.month, int):
            month = (None, str(self.month).encode(), "text/plain")
        else:
            month = (None, str(self.month).encode(), "text/plain")

        month_date: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.month_date, Unset):
            month_date = UNSET
        elif isinstance(self.month_date, datetime.date):
            month_date = self.month_date.isoformat().encode()
        else:
            month_date = (None, str(self.month_date).encode(), "text/plain")

        bank = (
            self.bank
            if isinstance(self.bank, Unset)
            else (None, str(self.bank).encode(), "text/plain")
        )

        identifier: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.identifier, Unset):
            identifier = UNSET
        elif isinstance(self.identifier, str):
            identifier = (None, str(self.identifier).encode(), "text/plain")
        else:
            identifier = (None, str(self.identifier).encode(), "text/plain")

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

        tag: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.tag, Unset):
            tag = UNSET
        elif isinstance(self.tag, int):
            tag = (None, str(self.tag).encode(), "text/plain")
        else:
            tag = (None, str(self.tag).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "tag_name": tag_name,
                "date": date,
                "name": name,
                "value": value,
            }
        )
        if month is not UNSET:
            field_dict["month"] = month
        if month_date is not UNSET:
            field_dict["month_date"] = month_date
        if bank is not UNSET:
            field_dict["bank"] = bank
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if user is not UNSET:
            field_dict["user"] = user
        if credential is not UNSET:
            field_dict["credential"] = credential
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        tag_name = d.pop("tag_name")

        date = isoparse(d.pop("date")).date()

        name = d.pop("name")

        value = d.pop("value")

        def _parse_month(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        month = _parse_month(d.pop("month", UNSET))

        def _parse_month_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                month_date_type_0 = isoparse(data).date()

                return month_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        month_date = _parse_month_date(d.pop("month_date", UNSET))

        bank = d.pop("bank", UNSET)

        def _parse_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        identifier = _parse_identifier(d.pop("identifier", UNSET))

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

        def _parse_tag(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        tag = _parse_tag(d.pop("tag", UNSET))

        transaction_rest = cls(
            id=id,
            tag_name=tag_name,
            date=date,
            name=name,
            value=value,
            month=month,
            month_date=month_date,
            bank=bank,
            identifier=identifier,
            user=user,
            credential=credential,
            tag=tag,
        )

        transaction_rest.additional_properties = d
        return transaction_rest

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
