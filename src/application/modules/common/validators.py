from datetime import datetime, timezone

from src.application.modules.common.exceptions import (
    InvalidDateFormat,
    InvalidDateRange,
)


def validate_date_format_from_string(date: str) -> None:
    try:
        datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise InvalidDateFormat from exc


def validate_date_format_from_date_time(date: datetime) -> None:
    try:
        formatted_date = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_date = datetime.strptime(
            formatted_date, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise InvalidDateFormat from exc

    if date.tzinfo is None:
        raise InvalidDateFormat

    if date != parsed_date:
        raise InvalidDateFormat


def validate_date_range(start: datetime, end: datetime) -> None:
    if start > end:
        raise InvalidDateRange
