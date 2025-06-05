from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.summery_widgets_graphs import SummeryWidgetsGraphs


T = TypeVar("T", bound="SummeryWidgets")


@_attrs_define
class SummeryWidgets:
    """
    Attributes:
        graphs (SummeryWidgetsGraphs):
        average_expenses (float):
        average_income (float):
        number_of_months (int):
        average_bank_expenses (float):
    """

    graphs: "SummeryWidgetsGraphs"
    average_expenses: float
    average_income: float
    number_of_months: int
    average_bank_expenses: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        graphs = self.graphs.to_dict()

        average_expenses = self.average_expenses

        average_income = self.average_income

        number_of_months = self.number_of_months

        average_bank_expenses = self.average_bank_expenses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "graphs": graphs,
                "average_expenses": average_expenses,
                "average_income": average_income,
                "number_of_months": number_of_months,
                "average_bank_expenses": average_bank_expenses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.summery_widgets_graphs import SummeryWidgetsGraphs

        d = dict(src_dict)
        graphs = SummeryWidgetsGraphs.from_dict(d.pop("graphs"))

        average_expenses = d.pop("average_expenses")

        average_income = d.pop("average_income")

        number_of_months = d.pop("number_of_months")

        average_bank_expenses = d.pop("average_bank_expenses")

        summery_widgets = cls(
            graphs=graphs,
            average_expenses=average_expenses,
            average_income=average_income,
            number_of_months=number_of_months,
            average_bank_expenses=average_bank_expenses,
        )

        summery_widgets.additional_properties = d
        return summery_widgets

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
