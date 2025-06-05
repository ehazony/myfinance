from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MonthCategory")


@_attrs_define
class MonthCategory:
    """
    Attributes:
        category_id (int):
        category (str):
        key (str):
        value (float):
        goal (int):
        type_ (str):
        percent (float):
        color (str):
    """

    category_id: int
    category: str
    key: str
    value: float
    goal: int
    type_: str
    percent: float
    color: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category_id = self.category_id

        category = self.category

        key = self.key

        value = self.value

        goal = self.goal

        type_ = self.type_

        percent = self.percent

        color = self.color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category_id": category_id,
                "category": category,
                "key": key,
                "value": value,
                "goal": goal,
                "type": type_,
                "percent": percent,
                "color": color,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category_id = d.pop("category_id")

        category = d.pop("category")

        key = d.pop("key")

        value = d.pop("value")

        goal = d.pop("goal")

        type_ = d.pop("type")

        percent = d.pop("percent")

        color = d.pop("color")

        month_category = cls(
            category_id=category_id,
            category=category,
            key=key,
            value=value,
            goal=goal,
            type_=type_,
            percent=percent,
            color=color,
        )

        month_category.additional_properties = d
        return month_category

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
