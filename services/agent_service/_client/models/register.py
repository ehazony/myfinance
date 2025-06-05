from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Register")


@_attrs_define
class Register:
    """
    Attributes:
        email (str):
        password1 (str):
        password2 (str):
        username (Union[Unset, str]):
    """

    email: str
    password1: str
    password2: str
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password1 = self.password1

        password2 = self.password2

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password1": password1,
                "password2": password2,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        email = (None, str(self.email).encode(), "text/plain")

        password1 = (None, str(self.password1).encode(), "text/plain")

        password2 = (None, str(self.password2).encode(), "text/plain")

        username = (
            self.username
            if isinstance(self.username, Unset)
            else (None, str(self.username).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "email": email,
                "password1": password1,
                "password2": password2,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        password1 = d.pop("password1")

        password2 = d.pop("password2")

        username = d.pop("username", UNSET)

        register = cls(
            email=email,
            password1=password1,
            password2=password2,
            username=username,
        )

        register.additional_properties = d
        return register

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
