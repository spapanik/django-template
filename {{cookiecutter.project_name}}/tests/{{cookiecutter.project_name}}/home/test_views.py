from http import HTTPStatus

from tests.conftest import HttpTestClient


def test_admin(http_client: HttpTestClient) -> None:
    response = http_client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert dir(response) == "home/index.html"
