import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.credential_types_fields_item import CredentialTypesFieldsItem


T = TypeVar("T", bound="CredentialTypes")


@_attrs_define
class CredentialTypes:
    """
    Attributes:
        key (str):
        name (str):
        fields (list['CredentialTypesFieldsItem']):
    """

    key: str
    name: str
    fields: list["CredentialTypesFieldsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        name = self.name

        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "name": name,
                "fields": fields,
            }
        )

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        key = (None, str(self.key).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        _temp_fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            _temp_fields.append(fields_item)
        fields = (None, json.dumps(_temp_fields).encode(), "application/json")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "key": key,
                "name": name,
                "fields": fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.credential_types_fields_item import CredentialTypesFieldsItem

        d = dict(src_dict)
        key = d.pop("key")

        name = d.pop("name")

        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = CredentialTypesFieldsItem.from_dict(fields_item_data)

            fields.append(fields_item)

        credential_types = cls(
            key=key,
            name=name,
            fields=fields,
        )

        credential_types.additional_properties = d
        return credential_types

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
