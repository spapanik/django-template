from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar, Self

from pathurl import URL

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest
from django.urls import reverse

from {{cookiecutter.project_name}}.lib.date_utils import now
from {{cookiecutter.project_name}}.lib.models import BaseModel, BaseQuerySet, OneToOneField
from {{cookiecutter.project_name}}.lib.utils import JWT, get_app_url


class UserManager(BaseUserManager.from_queryset(BaseQuerySet["User"])):  # type: ignore[misc]
    use_in_migrations = True

    def _create_user(
        self, email: str, password: str | None, **extra_fields: Any
    ) -> User:
        if not email:
            msg = "An email must be set"
            raise ValueError(msg)

        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class SignupTokenQuerySet(BaseQuerySet["SignupToken"]):
    def expired(self, as_of: datetime | None = None) -> SignupTokenQuerySet:
        as_of = as_of or now()
        return self.filter(created_at__lte=as_of - settings.SIGNUP_TOKEN_EXPIRY)


class SignupTokenManager(models.Manager.from_queryset(SignupTokenQuerySet)):  # type: ignore[misc]
    pass


class User(AbstractUser, BaseModel):
    username = None  # type: ignore[assignment]
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self) -> str:
        return self.email

    @classmethod
    def from_request(cls, request: HttpRequest) -> Self:
        bearer = request.META.get("HTTP_AUTHORIZATION")
        if not bearer:
            msg = "No bearer token"
            raise LookupError(msg)

        _, token = bearer.split()
        jwt = JWT.from_token(token)
        if jwt.sub != "access":
            msg = "Not an access token"
            raise LookupError(msg)

        try:
            user: Self = cls.objects.get_by_oid(jwt.id)
        except cls.DoesNotExist as exc:
            msg = "No such user"
            raise LookupError(msg) from exc

        return user

    def get_tokens(self) -> dict[str, str]:
        refresh_token = JWT.for_user(self, "refresh")
        access_token = JWT.for_user(self, "access")
        return {
            "refresh": str(refresh_token),
            "access": str(access_token),
        }

    def get_signup_token(self) -> SignupToken:
        """
        Get the signup token for this user.

        If one already exists, delete it first. This is to prevent
        expanding the lifetime of a token after the 24h limit.
        """
        SignupToken.objects.filter(user=self).delete()
        signup_token: SignupToken = SignupToken.objects.create(user=self)
        return signup_token


class SignupToken(BaseModel):
    user = OneToOneField(User, related_name="signup_token")

    objects: ClassVar[SignupTokenManager] = SignupTokenManager()

    @property
    def expired(self, as_of: datetime | None = None) -> bool:
        as_of = as_of or now()
        return self.created_at <= as_of - settings.SIGNUP_TOKEN_EXPIRY

    @property
    def signup_link(self) -> URL:
        return get_app_url(reverse("users:confirm-email", kwargs={"token": self.oid}))

    def __str__(self) -> str:
        return f"Signup token for {self.user}"
