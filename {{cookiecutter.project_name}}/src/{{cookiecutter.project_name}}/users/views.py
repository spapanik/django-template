from http import HTTPStatus
from typing import Any, cast

from joselib.exceptions import JWTError
from pathurl import URL

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpRequest

from {{cookiecutter.project_name}}.lib.emails import TransactionalEmail
from {{cookiecutter.project_name}}.lib.exceptions import ValidationError
from {{cookiecutter.project_name}}.lib.http import JsonResponse
from {{cookiecutter.project_name}}.lib.utils import JWT
from {{cookiecutter.project_name}}.lib.views import BaseAPIView
from {{cookiecutter.project_name}}.users.models import SignupToken, User


class TokenView(BaseAPIView):
    def _authenticate(self, data: dict[str, Any]) -> User | None:  # noqa: ARG002
        msg = f"{type(self).__qualname__}._authenticate is missing."
        raise NotImplementedError(msg)

    def _get_user_data(self, data: dict[str, Any]) -> dict[str, Any]:  # noqa: ARG002
        msg = f"{type(self).__qualname__}._get_user_data is missing."
        raise NotImplementedError(msg)

    def post(self, _request: HttpRequest) -> JsonResponse:
        try:
            body = cast(dict[str, Any], self.json_body())
            data = self._get_user_data(body)
        except ValidationError:
            return JsonResponse(
                {"error": {"message": "Invalid credentials."}},
                status=HTTPStatus.UNAUTHORIZED,
            )

        if (user := self._authenticate(data)) is None:
            return JsonResponse(
                {"error": {"message": "Invalid credentials."}},
                status=HTTPStatus.UNAUTHORIZED,
            )
        return JsonResponse(user.get_tokens())


class ObtainTokensView(TokenView):
    def _get_user_data(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "email": data.get("email", "").lower(),
            "password": data.get("password", ""),
        }

    def _authenticate(self, data: dict[str, Any]) -> User | None:
        return cast(
            User | None, authenticate(email=data["email"], password=data["password"])
        )


class RefreshTokenView(TokenView):
    def _get_user_data(self, data: dict[str, Any]) -> dict[str, Any]:
        refresh_token = data.get("token")
        if not refresh_token:
            msg = "Missing refresh token"
            raise ValidationError(msg)

        try:
            token = JWT.from_token(refresh_token)
        except JWTError as exc:
            msg = "Invalid refresh token"
            raise ValidationError(msg) from exc
        if token.sub != "refresh":
            msg = "Not a refresh token"
            raise ValidationError(msg)
        return {"refresh_token": token}

    def _authenticate(self, data: dict[str, Any]) -> User | None:
        refresh_token = data["refresh_token"]
        try:
            return cast(User, User.objects.get_by_oid(refresh_token.id))
        except User.DoesNotExist:
            return None


class UserAPIView(BaseAPIView):
    @staticmethod
    def send_confirmation_email(user: User) -> URL:
        signup_link = user.get_signup_token().signup_link
        TransactionalEmail.send_email(
            recipient=user,
            subject="Confirm your email",
            message=f"Please follow {signup_link} to complete the signup process.",
        )
        return signup_link

    def _get_user_info(self, item: dict[str, Any]) -> dict[str, Any]:
        email = item.get("email", "").lower()
        try:
            validate_email(email)
        except DjangoValidationError as exc:
            msg = "Invalid email address"
            raise ValidationError(msg) from exc

        password = item.get("password", "")
        try:
            validate_password(password)
        except DjangoValidationError as exc:
            msg = "Invalid password"
            raise ValidationError(msg, notes=exc.messages) from exc
        return {"email": email, "password": password, "is_active": False}

    def post(self, _request: HttpRequest) -> JsonResponse:
        try:
            body = cast(dict[str, Any], self.json_body())
            user_info = self._get_user_info(body)
        except ValidationError as exc:
            return JsonResponse(
                {"error": {"message": str(exc)}}, status=HTTPStatus.BAD_REQUEST
            )
        try:
            user = User.objects.create_user(**user_info)
        except IntegrityError as exc:
            return JsonResponse(
                {"error": {"message": str(exc)}}, status=HTTPStatus.CONFLICT
            )
        self.send_confirmation_email(user)
        return JsonResponse({"message": "OK"}, status=HTTPStatus.CREATED)


class ConfirmEmailAPIView(BaseAPIView):
    @staticmethod
    def post(_request: HttpRequest, token: int) -> JsonResponse:
        try:
            signup_token = SignupToken.objects.get_by_oid(token)
        except SignupToken.DoesNotExist:
            return JsonResponse(
                {"error": {"message": "Invalid token."}}, status=HTTPStatus.NOT_FOUND
            )
        if signup_token.expired:
            return JsonResponse(
                {"error": {"message": "Invalid token."}}, status=HTTPStatus.UNAUTHORIZED
            )
        user = signup_token.user
        user.is_active = True
        user.save()
        signup_token.delete()
        return JsonResponse(None, status=HTTPStatus.NO_CONTENT, safe=False)
