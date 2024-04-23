from collections.abc import Callable
from typing import Any, Literal

from django.db import models
from django.db.models.deletion import Collector

APIVerbs = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"]
JSONType = None | bool | int | float | str | list[Any] | dict[str, Any]
OnDeleteType = Callable[
    [Collector, Any, models.QuerySet[models.Model], str],
    None,
]
