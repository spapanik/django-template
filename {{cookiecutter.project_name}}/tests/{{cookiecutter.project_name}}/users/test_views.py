import pytest

from {{cookiecutter.project_name}}.users.models import User

from tests.{{cookiecutter.project_name}}.factories.users import SignupTokenFactory, UserFactory
from tests.conftest import JsonTestClient


class TestUserAPIView:
    @staticmethod
    @pytest.mark.django_db()
    def test_can_create_users(json_client: JsonTestClient) -> None:
        response = json_client.post(
            "/api/users/",
            data={
                "email": "arya@winterfell.gov",
                "password": "'EU6zY?lZl{3H4]s_^M~>f*`x",
            },
        )
        assert response.status_code == 201
        data = response.data
        assert isinstance(data, dict)
        assert data["message"] == "OK"

    @staticmethod
    @pytest.mark.parametrize(
        "email",
        [
            "arya-at-winterfell.gov",
            "arya@winterfell",
            "@winterfell.gov",
        ],
    )
    @pytest.mark.django_db()
    def test_cannot_create_user_with_invalid_email(
        json_client: JsonTestClient, email: str
    ) -> None:
        response = json_client.post(
            "/api/users/",
            data={"email": email, "password": "'EU6zY?lZl{3H4]s_^M~>f*`x"},
        )
        assert response.status_code == 400
        data = response.data
        assert isinstance(data, dict)
        assert data["error"]["message"] == "Invalid email address"

    @staticmethod
    @pytest.mark.django_db()
    def test_cannot_create_user_with_existing_email(
        json_client: JsonTestClient,
    ) -> None:
        email = "arya@winterfell.gov"
        user = UserFactory.build(email=email)
        user.save()
        response = json_client.post(
            "/api/users/",
            data={"email": email, "password": "'EU6zY?lZl{3H4]s_^M~>f*`x"},
        )
        assert response.status_code == 409
        data = response.data
        assert isinstance(data, dict)
        message_lines = data["error"]["message"].splitlines()
        assert len(message_lines) == 2
        assert (
            message_lines[0]
            == 'duplicate key value violates unique constraint "users_user_email_key"'
        )
        assert message_lines[1].startswith("DETAIL:  Key (email)=")

    @staticmethod
    @pytest.mark.parametrize(
        "password",
        [
            "password",
            "122128374912763584172364",
            "k4.1!JJ",
        ],
    )
    @pytest.mark.django_db()
    def test_cannot_create_user_with_invalid_password(
        json_client: JsonTestClient, password: str
    ) -> None:
        response = json_client.post(
            "/api/users/",
            data={"email": "arya@winterfell.gov", "password": password},
        )
        assert response.status_code == 400
        data = response.data
        assert isinstance(data, dict)
        assert data["error"]["message"] == "Invalid password"


class TestConfirmEmailAPIView:
    @staticmethod
    @pytest.mark.django_db()
    def test_email_confirmation_activates_user(json_client: JsonTestClient) -> None:
        user = UserFactory.build(is_active=False)
        user.save()
        signup_token = SignupTokenFactory.build(user=user)
        signup_token.save()
        response = json_client.post(
            f"/api/users/confirm-email/{signup_token.oid}",
        )
        assert response.status_code == 204
        assert response.data is None
        user = User.objects.get(id=user.id)
        assert user.is_active

    @staticmethod
    @pytest.mark.django_db()
    def test_cannot_activate_user_without_valid_token(
        json_client: JsonTestClient,
    ) -> None:
        user = UserFactory.build(is_active=False)
        user.save()
        signup_token = SignupTokenFactory.build(user=user)
        signup_token.save()
        response = json_client.post(
            f"/api/users/confirm-email/{signup_token.oid + 1}",
        )
        assert response.status_code == 404
        data = response.data
        assert isinstance(data, dict)
        assert not user.is_active


class TestObtainTokenAPIView:
    @staticmethod
    @pytest.mark.django_db()
    def test_users_can_obtain_tokens(json_client: JsonTestClient) -> None:
        user = UserFactory.build()
        user.set_password("strong_password")
        user.save()
        response = json_client.post(
            "/api/users/token/",
            data={"email": user.email, "password": "strong_password"},
        )
        assert response.status_code == 200

    @staticmethod
    @pytest.mark.django_db()
    def test_users_cannot_obtain_tokens_with_wrong_password(
        json_client: JsonTestClient,
    ) -> None:
        user = UserFactory.build()
        user.set_password("strong_password")
        user.save()
        response = json_client.post(
            "/api/users/token/",
            data={"email": user.email, "password": "password"},
        )
        assert response.status_code == 401

    @staticmethod
    @pytest.mark.django_db()
    def test_users_cannot_obtain_tokens_without_password(
        json_client: JsonTestClient,
    ) -> None:
        user = UserFactory.build()
        user.save()
        response = json_client.post(
            "/api/users/token/",
            data={"email": user.email},
        )
        assert response.status_code == 401


class TestRefreshTokenAPIView:
    @staticmethod
    @pytest.mark.django_db()
    def test_users_can_refresh_tokens(json_client: JsonTestClient) -> None:
        user = UserFactory.build()
        user.save()
        tokens = user.get_tokens()
        response = json_client.post(
            "/api/users/token/refresh",
            data={"token": tokens["refresh"]},
        )
        assert response.status_code == 200

    @staticmethod
    @pytest.mark.django_db()
    def test_users_cannot_refresh_tokens_with_access_token(
        json_client: JsonTestClient,
    ) -> None:
        user = UserFactory.build()
        user.save()
        tokens = user.get_tokens()
        response = json_client.post(
            "/api/users/token/refresh",
            data={"token": tokens["access"]},
        )
        assert response.status_code == 401
