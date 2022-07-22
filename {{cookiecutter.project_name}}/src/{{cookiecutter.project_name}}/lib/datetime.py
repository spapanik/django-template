import typing as tp
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from {{cookiecutter.project_name}}.lib.data.timezones import (
    DEPRECATED_TIMEZONES,
    NON_IANA_TIMEZONES,
    PROPOSED_TIMEZONES,
)

UTC = ZoneInfo("UTC")


def get_timezones() -> tp.Set[str]:
    unavailable_timezones = set.union(
        DEPRECATED_TIMEZONES, NON_IANA_TIMEZONES, PROPOSED_TIMEZONES
    )
    return available_timezones() - unavailable_timezones


def now(tz_info: ZoneInfo = UTC) -> datetime:
    return datetime.now(UTC).astimezone(tz_info)


def as_timezone(dt: datetime, tz_info: ZoneInfo = UTC) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz_info)
    return dt.astimezone(tz_info)
