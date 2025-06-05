import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.message import Message


T = TypeVar("T", bound="ConversationContext")


@_attrs_define
class ConversationContext:
    """User conversation context.

    Attributes:
        conversation_id (Union[None, int]):
        message_count (int):
        last_activity (Union[None, datetime.datetime]):
        recent_topics (list[str]):
        recent_messages (list['Message']):
    """

    conversation_id: Union[None, int]
    message_count: int
    last_activity: Union[None, datetime.datetime]
    recent_topics: list[str]
    recent_messages: list["Message"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conversation_id: Union[None, int]
        conversation_id = self.conversation_id

        message_count = self.message_count

        last_activity: Union[None, str]
        if isinstance(self.last_activity, datetime.datetime):
            last_activity = self.last_activity.isoformat()
        else:
            last_activity = self.last_activity

        recent_topics = self.recent_topics

        recent_messages = []
        for recent_messages_item_data in self.recent_messages:
            recent_messages_item = recent_messages_item_data.to_dict()
            recent_messages.append(recent_messages_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_id": conversation_id,
                "message_count": message_count,
                "last_activity": last_activity,
                "recent_topics": recent_topics,
                "recent_messages": recent_messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message import Message

        d = dict(src_dict)

        def _parse_conversation_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        conversation_id = _parse_conversation_id(d.pop("conversation_id"))

        message_count = d.pop("message_count")

        def _parse_last_activity(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_activity_type_0 = isoparse(data)

                return last_activity_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_activity = _parse_last_activity(d.pop("last_activity"))

        recent_topics = cast(list[str], d.pop("recent_topics"))

        recent_messages = []
        _recent_messages = d.pop("recent_messages")
        for recent_messages_item_data in _recent_messages:
            recent_messages_item = Message.from_dict(recent_messages_item_data)

            recent_messages.append(recent_messages_item)

        conversation_context = cls(
            conversation_id=conversation_id,
            message_count=message_count,
            last_activity=last_activity,
            recent_topics=recent_topics,
            recent_messages=recent_messages,
        )

        conversation_context.additional_properties = d
        return conversation_context

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
