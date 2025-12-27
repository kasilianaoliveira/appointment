from enum import StrEnum


class DateFilter(StrEnum):
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"


class FutureDateFilter(StrEnum):
    NEXT_7_DAYS = "next_7_days"
    NEXT_30_DAYS = "next_30_days"
    NEXT_90_DAYS = "next_90_days"
