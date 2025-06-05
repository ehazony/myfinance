from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDetails")


@_attrs_define
class UserDetails:
    """User model w/o password

    Attributes:
        pk (int):
        username (str): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        email (str):
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
    """

    pk: int
    username: str
    email: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pk = self.pk

        username = self.username

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pk": pk,
                "username": username,
                "email": email,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        pk = (None, str(self.pk).encode(), "text/plain")

        username = (None, str(self.username).encode(), "text/plain")

        email = (None, str(self.email).encode(), "text/plain")

        first_name = (
            self.first_name
            if isinstance(self.first_name, Unset)
            else (None, str(self.first_name).encode(), "text/plain")
        )

        last_name = (
            self.last_name
            if isinstance(self.last_name, Unset)
            else (None, str(self.last_name).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "pk": pk,
                "username": username,
                "email": email,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pk = d.pop("pk")

        username = d.pop("username")

        email = d.pop("email")

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        user_details = cls(
            pk=pk,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user_details.additional_properties = d
        return user_details

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
