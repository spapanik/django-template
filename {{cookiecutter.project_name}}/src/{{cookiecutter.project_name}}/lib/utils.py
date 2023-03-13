import hashlib
import logging
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any, ParamSpec

from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.writer import MigrationWriter

logger = logging.getLogger(__name__)
INGEST_ERROR = "Function `%s` threw `%s` when called with args=%s and kwargs=%s"
P = ParamSpec("P")


def handle_exceptions(
    *,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    default: Any = None,
    log_level: str = "info",
) -> Any:
    def decorator(func: Callable[P, Any]) -> Callable[P, Any]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                getattr(logger, log_level)(
                    INGEST_ERROR,
                    func.__name__,
                    exc.__class__.__name__,
                    args,
                    kwargs,
                    exc_info=True,
                )
                return default

        return wrapper

    return decorator


def hash_file(path: Path, buffer_size: int = 2**16) -> str:
    sha256 = hashlib.sha256()

    with path.open("rb") as f:
        while data := f.read(buffer_size):
            sha256.update(data)

    return sha256.hexdigest()


def hash_migrations() -> list[str]:
    loader = MigrationLoader(None, ignore_no_migrations=True)
    hashes = []
    source = settings.BASE_DIR.joinpath("src").as_posix()
    for (app, migration_name), migration in loader.graph.nodes.items():
        path = MigrationWriter(migration).path
        if path.startswith(source):
            hashes.append(f"{app}::{migration_name}::{hash_file(Path(path))}")
    return sorted(hashes)
