import hashlib
import logging
from functools import wraps
from pathlib import Path
from typing import Any, Callable, List, Tuple, Type

from django.db.migrations.loader import MigrationLoader
from django.db.migrations.writer import MigrationWriter

logger = logging.getLogger(__name__)
INGEST_ERROR = "Function `%s` threw `%s` when called with args=%s and kwargs=%s"


def handle_exceptions(
    *,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    default: Any = None,
    log_level: str = "info",
) -> Any:
    def decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
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


def hash_file(path: Path | str, buffer_size=2**16) -> str:
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def hash_migrations() -> List[str]:
    loader = MigrationLoader(None, ignore_no_migrations=True)
    hashes = []
    for (app, migration_name), migration in loader.graph.nodes.items():
        path = MigrationWriter(migration).path
        hashes.append(f"{app}::{migration_name}::{hash_file(path)}")
    return sorted(hashes)
