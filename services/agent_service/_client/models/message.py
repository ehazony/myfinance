import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        id (int):
        sender (str):
        content (str):
        timestamp (datetime.datetime):
        content_type (Union[Unset, str]):
        payload (Union[Unset, Any]):
    """

    id: int
    sender: str
    content: str
    timestamp: datetime.datetime
    content_type: Union[Unset, str] = UNSET
    payload: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sender = self.sender

        content = self.content

        timestamp = self.timestamp.isoformat()

        content_type = self.content_type

        payload = self.payload

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sender": sender,
                "content": content,
                "timestamp": timestamp,
            }
        )
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        sender = d.pop("sender")

        content = d.pop("content")

        timestamp = isoparse(d.pop("timestamp"))

        content_type = d.pop("content_type", UNSET)

        payload = d.pop("payload", UNSET)

        message = cls(
            id=id,
            sender=sender,
            content=content,
            timestamp=timestamp,
            content_type=content_type,
            payload=payload,
        )

        message.additional_properties = d
        return message

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
