from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time

from {{cookiecutter.project_name}}.lib import date_utils

TEST_TIMEZONES = [ZoneInfo("UTC"), ZoneInfo("Europe/London"), ZoneInfo("Asia/Tokyo")]


@freeze_time("2012-01-14 12:00:01")
def test_now():
    now = date_utils.now()
    assert now.tzinfo == ZoneInfo("UTC")
    assert now.timestamp() == datetime.utcnow().timestamp()


def test_get_timezones():
    all_timezones = date_utils.get_timezones()
    assert "UTC" in all_timezones
    assert "Europe/Zurich" in all_timezones


@pytest.mark.parametrize(
    "date_string",
    [
        "2022-01-01T00:00:00Z",
        "2022-01-01T00:00:00+00:00",
    ],
)
@pytest.mark.parametrize("tz_info", TEST_TIMEZONES)
def test_from_iso(date_string, tz_info):
    dt = date_utils.from_iso(date_string, tz_info)
    assert dt.tzinfo == tz_info
    assert dt.timestamp() == 1640995200


@pytest.mark.parametrize("tz_info", TEST_TIMEZONES)
def test_from_timestamp(tz_info):
    dt = date_utils.from_timestamp(0, tz_info)
    assert dt.tzinfo == tz_info
    assert dt.timestamp() == 0


@pytest.mark.parametrize(
    ["tz_info", "expected"],
    [
        [ZoneInfo("UTC"), datetime(2022, 1, 1, tzinfo=ZoneInfo("UTC"))],
        [ZoneInfo("Europe/London"), datetime(2022, 1, 1, tzinfo=ZoneInfo("UTC"))],
        [ZoneInfo("Asia/Tokyo"), datetime(2021, 12, 31, 15, tzinfo=ZoneInfo("UTC"))],
    ],
)
def test_add_timezone_to_naive_datetime(tz_info, expected):
    dt = datetime(2022, 1, 1)
    assert date_utils.add_timezone(dt, tz_info) == expected


def test_add_timezone_to_tz_aware_datetime():
    pytest.raises(
        ValueError,
        date_utils.add_timezone,
        datetime(2022, 1, 1, tzinfo=ZoneInfo("UTC")),
    )


@pytest.mark.parametrize("tz_info", TEST_TIMEZONES)
def test_convert_does_not_change_timestamp(tz_info):
    dt = datetime(2022, 1, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert date_utils.convert_timezone(dt, tz_info) == dt


def test_convert_timezone_to_naive_datetime():
    pytest.raises(
        ValueError,
        date_utils.convert_timezone,
        datetime(2022, 1, 1),
    )
