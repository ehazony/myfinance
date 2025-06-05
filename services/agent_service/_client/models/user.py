import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        id (int):
        password (str):
        username (str): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        last_login (Union[None, Unset, datetime.datetime]):
        is_superuser (Union[Unset, bool]): Designates that this user has all permissions without explicitly assigning
            them.
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        email (Union[Unset, str]):
        is_staff (Union[Unset, bool]): Designates whether the user can log into this admin site.
        is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Unselect this instead
            of deleting accounts.
        date_joined (Union[Unset, datetime.datetime]):
        groups (Union[Unset, list[int]]): The groups this user belongs to. A user will get all permissions granted to
            each of their groups.
        user_permissions (Union[Unset, list[int]]): Specific permissions for this user.
    """

    id: int
    password: str
    username: str
    last_login: Union[None, Unset, datetime.datetime] = UNSET
    is_superuser: Union[Unset, bool] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    is_staff: Union[Unset, bool] = UNSET
    is_active: Union[Unset, bool] = UNSET
    date_joined: Union[Unset, datetime.datetime] = UNSET
    groups: Union[Unset, list[int]] = UNSET
    user_permissions: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        password = self.password

        username = self.username

        last_login: Union[None, Unset, str]
        if isinstance(self.last_login, Unset):
            last_login = UNSET
        elif isinstance(self.last_login, datetime.datetime):
            last_login = self.last_login.isoformat()
        else:
            last_login = self.last_login

        is_superuser = self.is_superuser

        first_name = self.first_name

        last_name = self.last_name

        email = self.email

        is_staff = self.is_staff

        is_active = self.is_active

        date_joined: Union[Unset, str] = UNSET
        if not isinstance(self.date_joined, Unset):
            date_joined = self.date_joined.isoformat()

        groups: Union[Unset, list[int]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        user_permissions: Union[Unset, list[int]] = UNSET
        if not isinstance(self.user_permissions, Unset):
            user_permissions = self.user_permissions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "password": password,
                "username": username,
            }
        )
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if is_superuser is not UNSET:
            field_dict["is_superuser"] = is_superuser
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if date_joined is not UNSET:
            field_dict["date_joined"] = date_joined
        if groups is not UNSET:
            field_dict["groups"] = groups
        if user_permissions is not UNSET:
            field_dict["user_permissions"] = user_permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        password = d.pop("password")

        username = d.pop("username")

        def _parse_last_login(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_login_type_0 = isoparse(data)

                return last_login_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_login = _parse_last_login(d.pop("last_login", UNSET))

        is_superuser = d.pop("is_superuser", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        email = d.pop("email", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        is_active = d.pop("is_active", UNSET)

        _date_joined = d.pop("date_joined", UNSET)
        date_joined: Union[Unset, datetime.datetime]
        if isinstance(_date_joined, Unset):
            date_joined = UNSET
        else:
            date_joined = isoparse(_date_joined)

        groups = cast(list[int], d.pop("groups", UNSET))

        user_permissions = cast(list[int], d.pop("user_permissions", UNSET))

        user = cls(
            id=id,
            password=password,
            username=username,
            last_login=last_login,
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=date_joined,
            groups=groups,
            user_permissions=user_permissions,
        )

        user.additional_properties = d
        return user

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
