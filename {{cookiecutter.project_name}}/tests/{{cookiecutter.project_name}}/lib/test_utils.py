import pytest

from {{cookiecutter.project_name}}.lib import utils


def test_handle_exceptions_expected_exception():
    @utils.handle_exceptions(exceptions=(ZeroDivisionError,), default="BOOM!")
    def invert(n):
        return 1 / n

    assert invert(1) == 1
    assert invert(0) == "BOOM!"


def test_handle_exceptions_unexpected_exception():
    @utils.handle_exceptions(exceptions=(TypeError,), default="BOOM!")
    def invert(n):
        return 1 / n

    assert invert(1) == 1
    pytest.raises(ZeroDivisionError, invert, 0)


def test_hash_file():
    dev_null_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert utils.hash_file("/dev/null") == dev_null_hash


def test_hash_migrations():
    hashed_migrations = {
        app: migration
        for app, migration, *_ in (h.split("::") for h in utils.hash_migrations())
    }
    assert "authentication" in hashed_migrations
    assert "0001_initial" in hashed_migrations["authentication"]
