import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """Transaction data for agents.

    Attributes:
        transaction_id (str):
        date (datetime.date):
        description (str):
        amount (float):
        currency (str):
        account_id (str):
        category (Union[None, str]):
        tags (list[str]):
    """

    transaction_id: str
    date: datetime.date
    description: str
    amount: float
    currency: str
    account_id: str
    category: Union[None, str]
    tags: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction_id = self.transaction_id

        date = self.date.isoformat()

        description = self.description

        amount = self.amount

        currency = self.currency

        account_id = self.account_id

        category: Union[None, str]
        category = self.category

        tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction_id": transaction_id,
                "date": date,
                "description": description,
                "amount": amount,
                "currency": currency,
                "account_id": account_id,
                "category": category,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_id = d.pop("transaction_id")

        date = isoparse(d.pop("date")).date()

        description = d.pop("description")

        amount = d.pop("amount")

        currency = d.pop("currency")

        account_id = d.pop("account_id")

        def _parse_category(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category = _parse_category(d.pop("category"))

        tags = cast(list[str], d.pop("tags"))

        transaction = cls(
            transaction_id=transaction_id,
            date=date,
            description=description,
            amount=amount,
            currency=currency,
            account_id=account_id,
            category=category,
            tags=tags,
        )

        transaction.additional_properties = d
        return transaction

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
