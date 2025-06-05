from enum import Enum


class TypeEnum(str, Enum):
    CONTINUOUS = "CONTINUOUS"
    MONTHLY_FIXED = "MONTHLY FIXED"
    PERIODIC = "PERIODIC"

    def __str__(self) -> str:
        return str(self.value)
