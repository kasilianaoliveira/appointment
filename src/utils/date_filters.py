from datetime import timedelta

from enums import DateFilter, FutureDateFilter

DATE_FILTERS = {
    DateFilter.LAST_7_DAYS: timedelta(days=7),
    DateFilter.LAST_30_DAYS: timedelta(days=30),
    DateFilter.LAST_90_DAYS: timedelta(days=90),
}

FUTURE_DATE_FILTERS = {
    FutureDateFilter.NEXT_7_DAYS: timedelta(days=7),
    FutureDateFilter.NEXT_30_DAYS: timedelta(days=30),
    FutureDateFilter.NEXT_90_DAYS: timedelta(days=90),
}


def get_date_filter(date_filter: DateFilter) -> timedelta:
    return DATE_FILTERS[date_filter]
