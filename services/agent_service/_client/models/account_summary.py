import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AccountSummary")


@_attrs_define
class AccountSummary:
    """Account summary data.

    Attributes:
        account_id (str):
        account_name (str):
        account_type (str):
        balance (Union[None, float]):
        last_transaction_date (Union[None, datetime.date]):
        transaction_count (int):
    """

    account_id: str
    account_name: str
    account_type: str
    balance: Union[None, float]
    last_transaction_date: Union[None, datetime.date]
    transaction_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        account_name = self.account_name

        account_type = self.account_type

        balance: Union[None, float]
        balance = self.balance

        last_transaction_date: Union[None, str]
        if isinstance(self.last_transaction_date, datetime.date):
            last_transaction_date = self.last_transaction_date.isoformat()
        else:
            last_transaction_date = self.last_transaction_date

        transaction_count = self.transaction_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "account_name": account_name,
                "account_type": account_type,
                "balance": balance,
                "last_transaction_date": last_transaction_date,
                "transaction_count": transaction_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_id = d.pop("account_id")

        account_name = d.pop("account_name")

        account_type = d.pop("account_type")

        def _parse_balance(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        balance = _parse_balance(d.pop("balance"))

        def _parse_last_transaction_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_transaction_date_type_0 = isoparse(data).date()

                return last_transaction_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        last_transaction_date = _parse_last_transaction_date(
            d.pop("last_transaction_date")
        )

        transaction_count = d.pop("transaction_count")

        account_summary = cls(
            account_id=account_id,
            account_name=account_name,
            account_type=account_type,
            balance=balance,
            last_transaction_date=last_transaction_date,
            transaction_count=transaction_count,
        )

        account_summary.additional_properties = d
        return account_summary

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
