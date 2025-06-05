from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.type_enum import TypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """
    Attributes:
        id (int):
        name (str):
        key (Union[None, Unset, str]):
        expense (Union[Unset, bool]):
        type_ (Union[Unset, TypeEnum]): * `MONTHLY FIXED` - MONTHLY FIXED
            * `PERIODIC` - PERIODIC
            * `CONTINUOUS` - CONTINUOUS
        user (Union[None, Unset, int]):
    """

    id: int
    name: str
    key: Union[None, Unset, str] = UNSET
    expense: Union[Unset, bool] = UNSET
    type_: Union[Unset, TypeEnum] = UNSET
    user: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        key: Union[None, Unset, str]
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        expense = self.expense

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        user: Union[None, Unset, int]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if expense is not UNSET:
            field_dict["expense"] = expense
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        key: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.key, Unset):
            key = UNSET
        elif isinstance(self.key, str):
            key = (None, str(self.key).encode(), "text/plain")
        else:
            key = (None, str(self.key).encode(), "text/plain")

        expense = (
            self.expense
            if isinstance(self.expense, Unset)
            else (None, str(self.expense).encode(), "text/plain")
        )

        type_: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = (None, str(self.type_.value).encode(), "text/plain")

        user: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.user, Unset):
            user = UNSET
        elif isinstance(self.user, int):
            user = (None, str(self.user).encode(), "text/plain")
        else:
            user = (None, str(self.user).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if expense is not UNSET:
            field_dict["expense"] = expense
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        key = _parse_key(d.pop("key", UNSET))

        expense = d.pop("expense", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TypeEnum(_type_)

        def _parse_user(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        user = _parse_user(d.pop("user", UNSET))

        tag = cls(
            id=id,
            name=name,
            key=key,
            expense=expense,
            type_=type_,
            user=user,
        )

        tag.additional_properties = d
        return tag

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
