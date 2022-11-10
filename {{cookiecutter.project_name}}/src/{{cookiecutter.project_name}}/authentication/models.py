from __future__ import annotations

from typing import List, Optional, cast

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from {{cookiecutter.project_name}}.lib.models import BaseManager, BaseModel, BaseQuerySet


class UserManager(BaseUserManager, BaseManager.from_queryset(BaseQuerySet)):  # type: ignore[misc]
    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        email: Optional[str],
        password: Optional[str],
        **extra_fields,
    ) -> User:
        """
        Create and save a user with the given username, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        username = self.normalize_email(username)
        user: User = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser, BaseModel):
    username: str = models.EmailField(unique=True)
    first_name = None
    last_name = None
    email = None

    EMAIL_FIELD = "username"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self) -> str:
        return self.username
