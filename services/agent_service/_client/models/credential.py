import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Credential")


@_attrs_define
class Credential:
    """
    Attributes:
        id (int):
        company (str):
        type_ (str):
        balance (str):
        last_scanned (Union[None, Unset, datetime.date]):
        additional_info (Union[Unset, Any]):
    """

    id: int
    company: str
    type_: str
    balance: str
    last_scanned: Union[None, Unset, datetime.date] = UNSET
    additional_info: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        company = self.company

        type_ = self.type_

        balance = self.balance

        last_scanned: Union[None, Unset, str]
        if isinstance(self.last_scanned, Unset):
            last_scanned = UNSET
        elif isinstance(self.last_scanned, datetime.date):
            last_scanned = self.last_scanned.isoformat()
        else:
            last_scanned = self.last_scanned

        additional_info = self.additional_info

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "company": company,
                "type": type_,
                "balance": balance,
            }
        )
        if last_scanned is not UNSET:
            field_dict["last_scanned"] = last_scanned
        if additional_info is not UNSET:
            field_dict["additional_info"] = additional_info

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        company = (None, str(self.company).encode(), "text/plain")

        type_ = (None, str(self.type_).encode(), "text/plain")

        balance = (None, str(self.balance).encode(), "text/plain")

        last_scanned: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.last_scanned, Unset):
            last_scanned = UNSET
        elif isinstance(self.last_scanned, datetime.date):
            last_scanned = self.last_scanned.isoformat().encode()
        else:
            last_scanned = (None, str(self.last_scanned).encode(), "text/plain")

        additional_info = (
            self.additional_info
            if isinstance(self.additional_info, Unset)
            else (None, str(self.additional_info).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "company": company,
                "type": type_,
                "balance": balance,
            }
        )
        if last_scanned is not UNSET:
            field_dict["last_scanned"] = last_scanned
        if additional_info is not UNSET:
            field_dict["additional_info"] = additional_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        company = d.pop("company")

        type_ = d.pop("type")

        balance = d.pop("balance")

        def _parse_last_scanned(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_scanned_type_0 = isoparse(data).date()

                return last_scanned_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        last_scanned = _parse_last_scanned(d.pop("last_scanned", UNSET))

        additional_info = d.pop("additional_info", UNSET)

        credential = cls(
            id=id,
            company=company,
            type_=type_,
            balance=balance,
            last_scanned=last_scanned,
            additional_info=additional_info,
        )

        credential.additional_properties = d
        return credential

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
