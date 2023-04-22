import pytest
from django.test import Client


class HttpTestClient(Client):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("HTTP_X_FORWARDED_PROTO", "https")
        super().__init__(*args, **kwargs)


@pytest.fixture()
def http_client() -> HttpTestClient:
    return HttpTestClient()
