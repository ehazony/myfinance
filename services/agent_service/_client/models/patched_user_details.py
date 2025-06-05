from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUserDetails")


@_attrs_define
class PatchedUserDetails:
    """User model w/o password

    Attributes:
        pk (Union[Unset, int]):
        username (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
    """

    pk: Union[Unset, int] = UNSET
    username: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
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
        field_dict.update({})
        if pk is not UNSET:
            field_dict["pk"] = pk
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        pk = (
            self.pk
            if isinstance(self.pk, Unset)
            else (None, str(self.pk).encode(), "text/plain")
        )

        username = (
            self.username
            if isinstance(self.username, Unset)
            else (None, str(self.username).encode(), "text/plain")
        )

        email = (
            self.email
            if isinstance(self.email, Unset)
            else (None, str(self.email).encode(), "text/plain")
        )

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

        field_dict.update({})
        if pk is not UNSET:
            field_dict["pk"] = pk
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pk = d.pop("pk", UNSET)

        username = d.pop("username", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        patched_user_details = cls(
            pk=pk,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        patched_user_details.additional_properties = d
        return patched_user_details

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
