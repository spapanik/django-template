from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from django.conf import settings

from {{cookiecutter.project_name}}.lib.data.timezones import UNAVAILABLE_TIMEZONES

UTC = ZoneInfo("UTC")


def now(local_timezone: ZoneInfo = settings.TZ_INFO) -> datetime:
    return datetime.now(ZoneInfo("UTC")).astimezone(local_timezone)

def get_timezones() -> set[str]:
    """
    Get all the available timezones

    This takes into accounts timezones that might not be present in
    all systems.
    """
    return available_timezones() - UNAVAILABLE_TIMEZONES


def from_iso(date_string: str, local_timezone: ZoneInfo = settings.TZ_INFO) -> datetime:
    """
    Get datetime from an iso string

    This to allow the Zulu timezone, which is a valid ISO timezone.
    """
    date_string = date_string.replace("Z", "+00:00")
    dt = datetime.fromisoformat(date_string)
    try:
        return add_timezone(dt, local_timezone)
    except ValueError:
        return convert_timezone(dt, local_timezone)


def from_timestamp(
    timestamp: float, local_timezone: ZoneInfo = settings.TZ_INFO
) -> datetime:
    """
    Get a datetime tz-aware time object from a timestamp
    """
    utc_dt = add_timezone(datetime.fromtimestamp(timestamp))
    return convert_timezone(utc_dt, local_timezone)


def add_timezone(dt: datetime, local_timezone: ZoneInfo = settings.TZ_INFO) -> datetime:
    """
    Add a timezone to a naive datetime

    Raise an error in case of a tz-aware datetime
    """
    if dt.tzinfo is not None:
        raise ValueError(f"{dt} is already tz-aware")
    return dt.replace(tzinfo=local_timezone)


def convert_timezone(
    dt: datetime, local_timezone: ZoneInfo = settings.TZ_INFO
) -> datetime:
    """
    Change the timezone of a tz-aware datetime

    Raise an error in case of a naive datetime
    """
    if dt.tzinfo is None:
        raise ValueError(f"{dt} is a naive datetime")
    return dt.astimezone(local_timezone)
