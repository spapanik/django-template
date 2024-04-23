from typing import Any, cast

import pytest

from django.test import Client

from {{cookiecutter.project_name}}.lib.http import JsonResponse


class JsonTestClient(Client):
    @staticmethod
    def _update_kwargs(kwargs: dict[str, Any]) -> None:
        # update content type
        kwargs.setdefault("content_type", "application/json")

        # make an HTTPS request by default
        kwargs.setdefault("secure", True)

        # update headers
        headers = kwargs.pop("headers", {})
        headers.setdefault("X_FORWARDED_PROTO", "https")
        if token := kwargs.pop("jwt_access_token", None):
            headers.setdefault("AUTHORIZATION", f"Bearer {token}")
        kwargs["headers"] = headers

    def get(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().get(*args, **kwargs))

    def post(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().post(*args, **kwargs))

    def put(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().put(*args, **kwargs))

    def patch(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().patch(*args, **kwargs))

    def delete(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().delete(*args, **kwargs))

    def head(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().head(*args, **kwargs))

    def options(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().options(*args, **kwargs))

    def trace(self, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore[override]
        self._update_kwargs(kwargs)
        return cast(JsonResponse, super().trace(*args, **kwargs))


@pytest.fixture()
def json_client() -> JsonTestClient:
    return JsonTestClient()
