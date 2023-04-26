import os
from collections import defaultdict
from pathlib import Path

import pytest
from django.conf import settings

from {{cookiecutter.project_name}}.lib import utils


def test_handle_exceptions_handled_exception() -> None:
    @utils.handle_exceptions(exceptions=(ZeroDivisionError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    assert invert(0) == 0


def test_handle_exceptions_unhandled_exception() -> None:
    @utils.handle_exceptions(exceptions=(TypeError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    pytest.raises(ZeroDivisionError, invert, 0)


def test_hash_file() -> None:
    dev_null_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert utils.hash_file(Path(os.devnull)) == dev_null_hash


def test_hash_migrations() -> None:
    hashed_migrations = defaultdict(list)
    for hashed_migration in utils.hash_migrations():
        app, name, _ = hashed_migration.split("::")
        hashed_migrations[app].append(name)
    assert "registration" in hashed_migrations
    assert "0001_initial" in hashed_migrations["registration"]
