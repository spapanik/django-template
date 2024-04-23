import hashlib
import logging
from collections.abc import Callable
from dataclasses import asdict, dataclass
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Literal, ParamSpec, Self, TypeVar, cast

from joselib import jwt
from pathurl import URL, Query

from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.writer import MigrationWriter

from {{cookiecutter.project_name}}.lib.date_utils import now

if TYPE_CHECKING:
    from {{cookiecutter.project_name}}.users.models import User

logger = logging.getLogger(__name__)
INGEST_ERROR = "Function `%s` threw `%s` when called with args=%s and kwargs=%s"
P = ParamSpec("P")
R_co = TypeVar("R_co", covariant=True)


@dataclass
class JWT:
    sub: Literal["access", "refresh"]
    id: int
    exp: int

    @classmethod
    def for_user(cls, user: "User", jwt_type: Literal["access", "refresh"]) -> Self:
        expiry_delta = (
            settings.REFRESH_TOKEN_EXPIRY
            if jwt_type == "refresh"
            else settings.ACCESS_TOKEN_EXPIRY
        )
        return cls(
            sub=jwt_type,
            id=user.oid,
            exp=int((now() + expiry_delta).timestamp()),
        )

    @classmethod
    def from_token(cls, token: str) -> Self:
        return cls(**jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]))  # type: ignore[no-untyped-call]

    def __str__(self) -> str:
        return cast(
            str, jwt.encode(asdict(self), settings.SECRET_KEY, algorithm="HS256")  # type: ignore[no-untyped-call]
        )


class Optimus:
    def __init__(self) -> None:
        self.max_int = 2**63 - 1
        self.prime: int = settings.OPTIMUS_PRIME
        self.inverse: int = settings.OPTIMUS_INVERSE
        self.random: int = settings.OPTIMUS_RANDOM

    def encode(self, n: int) -> int:
        return ((n * self.prime) % self.max_int) ^ self.random

    def decode(self, n: int) -> int:
        return ((n ^ self.random) * self.inverse) % self.max_int


def handle_exceptions(
    *,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    default: R_co | None = None,
    log_level: str = "info",
) -> Callable[[Callable[P, R_co]], Callable[P, R_co | None]]:
    def decorator(func: Callable[P, R_co]) -> Callable[P, R_co | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R_co | None:
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


def get_app_url(path: str, **kwargs: str | list[str]) -> URL:
    return URL.from_parts(
        scheme=settings.BASE_SCHEME,
        hostname=settings.BASE_APP_DOMAIN,
        port=settings.BASE_APP_PORT,
        path=path,
        query=Query.from_dict(dict_={}, **kwargs),
    )


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
