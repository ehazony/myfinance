from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.financial_context_budget_inputs import FinancialContextBudgetInputs
    from ..models.financial_context_budget_targets import FinancialContextBudgetTargets
    from ..models.financial_context_category_mapping import (
        FinancialContextCategoryMapping,
    )
    from ..models.financial_context_transactions_item import (
        FinancialContextTransactionsItem,
    )


T = TypeVar("T", bound="FinancialContext")


@_attrs_define
class FinancialContext:
    """Complete financial context for a user.

    Attributes:
        transactions (list['FinancialContextTransactionsItem']):
        category_mapping (FinancialContextCategoryMapping):
        budget_targets (FinancialContextBudgetTargets):
        budget_inputs (FinancialContextBudgetInputs):
        user_id (str):
        username (str):
    """

    transactions: list["FinancialContextTransactionsItem"]
    category_mapping: "FinancialContextCategoryMapping"
    budget_targets: "FinancialContextBudgetTargets"
    budget_inputs: "FinancialContextBudgetInputs"
    user_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        category_mapping = self.category_mapping.to_dict()

        budget_targets = self.budget_targets.to_dict()

        budget_inputs = self.budget_inputs.to_dict()

        user_id = self.user_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions": transactions,
                "category_mapping": category_mapping,
                "budget_targets": budget_targets,
                "budget_inputs": budget_inputs,
                "user_id": user_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.financial_context_budget_inputs import (
            FinancialContextBudgetInputs,
        )
        from ..models.financial_context_budget_targets import (
            FinancialContextBudgetTargets,
        )
        from ..models.financial_context_category_mapping import (
            FinancialContextCategoryMapping,
        )
        from ..models.financial_context_transactions_item import (
            FinancialContextTransactionsItem,
        )

        d = dict(src_dict)
        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = FinancialContextTransactionsItem.from_dict(
                transactions_item_data
            )

            transactions.append(transactions_item)

        category_mapping = FinancialContextCategoryMapping.from_dict(
            d.pop("category_mapping")
        )

        budget_targets = FinancialContextBudgetTargets.from_dict(
            d.pop("budget_targets")
        )

        budget_inputs = FinancialContextBudgetInputs.from_dict(d.pop("budget_inputs"))

        user_id = d.pop("user_id")

        username = d.pop("username")

        financial_context = cls(
            transactions=transactions,
            category_mapping=category_mapping,
            budget_targets=budget_targets,
            budget_inputs=budget_inputs,
            user_id=user_id,
            username=username,
        )

        financial_context.additional_properties = d
        return financial_context

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
