from __future__ import annotations

from typing import List, cast

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from {{cookiecutter.project_name}}.lib.models import BaseManager, BaseModel, BaseQuerySet


class UserManager(BaseUserManager, BaseManager.from_queryset(BaseQuerySet)):  # type: ignore[misc]
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> User:
        if not email:
            raise ValueError("An email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return cast(User, user)

    def create_user(self, email: str, password: str = None, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str = None, **extra_fields
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    first_name = None
    last_name = None
    email: str = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self) -> str:
        return self.email
