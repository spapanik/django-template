from datetime import datetime
from typing import Set
from zoneinfo import ZoneInfo, available_timezones

from {{cookiecutter.project_name}}.lib.data.timezones import UNAVAILABLE_TIMEZONES

UTC = ZoneInfo("UTC")


def get_timezones() -> Set[str]:
    """
    Get all the available timezones

    This takes into accounts timezones that might not be present in
    all systems.
    """
    return available_timezones() - UNAVAILABLE_TIMEZONES


def now(tz_info: ZoneInfo = UTC) -> datetime:
    return datetime.now(UTC).astimezone(tz_info)


def as_timezone(dt: datetime, tz_info: ZoneInfo = UTC) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz_info)
    return dt.astimezone(tz_info)
