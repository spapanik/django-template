from collections import defaultdict

import pytest

from django.test import override_settings

from {{cookiecutter.project_name}}.lib import utils


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
@override_settings(
    OPTIMUS_PRIME=3763233884940218597,
    OPTIMUS_INVERSE=8559198950554358756,
    OPTIMUS_RANDOM=2911243570405232861,
)
def test_optimus(n: int) -> None:
    optimus = utils.Optimus()
    encoded = optimus.encode(n)
    assert encoded != n
    assert optimus.decode(encoded) == n


@override_settings(BASE_APP_DOMAIN="www.example.com", BASE_APP_PORT=443)
@pytest.mark.parametrize(
    ("path", "kwargs", "expected"),
    [
        ("relative/path", {}, "https://www.example.com/relative/path"),
        ("/absolute/path", {}, "https://www.example.com/absolute/path"),
        (
            "relative/path",
            {"foo": "bar"},
            "https://www.example.com/relative/path?foo=bar",
        ),
    ],
)
def test_get_app_url(path: str, kwargs: dict[str, str], expected: str) -> None:
    assert utils.get_app_url(path, **kwargs).string == expected


def test_hash_migrations() -> None:
    hashed_migrations = defaultdict(list)
    for hashed_migration in utils.hash_migrations():
        app, name, _ = hashed_migration.split("::")
        hashed_migrations[app].append(name)
    assert "users" in hashed_migrations
    assert "0001_initial" in hashed_migrations["users"]
