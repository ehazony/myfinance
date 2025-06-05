from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BudgetTarget")


@_attrs_define
class BudgetTarget:
    """Budget target data.

    Attributes:
        category (str):
        target_amount (float):
        current_spent (float):
        remaining (float):
        progress_percentage (float):
    """

    category: str
    target_amount: float
    current_spent: float
    remaining: float
    progress_percentage: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category = self.category

        target_amount = self.target_amount

        current_spent = self.current_spent

        remaining = self.remaining

        progress_percentage = self.progress_percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category": category,
                "target_amount": target_amount,
                "current_spent": current_spent,
                "remaining": remaining,
                "progress_percentage": progress_percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category = d.pop("category")

        target_amount = d.pop("target_amount")

        current_spent = d.pop("current_spent")

        remaining = d.pop("remaining")

        progress_percentage = d.pop("progress_percentage")

        budget_target = cls(
            category=category,
            target_amount=target_amount,
            current_spent=current_spent,
            remaining=remaining,
            progress_percentage=progress_percentage,
        )

        budget_target.additional_properties = d
        return budget_target

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
