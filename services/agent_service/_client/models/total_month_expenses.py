from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TotalMonthExpenses")


@_attrs_define
class TotalMonthExpenses:
    """
    Attributes:
        moving_average (float):
        value (float):
        text (str):
        color (str):
    """

    moving_average: float
    value: float
    text: str
    color: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        moving_average = self.moving_average

        value = self.value

        text = self.text

        color = self.color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "moving_average": moving_average,
                "value": value,
                "text": text,
                "color": color,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        moving_average = d.pop("moving_average")

        value = d.pop("value")

        text = d.pop("text")

        color = d.pop("color")

        total_month_expenses = cls(
            moving_average=moving_average,
            value=value,
            text=text,
            color=color,
        )

        total_month_expenses.additional_properties = d
        return total_month_expenses

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
