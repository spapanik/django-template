from secrets import choice
from typing import Self

from django.db import models


class Choices(models.TextChoices):
    @classmethod
    def random(cls) -> Self:
        return choice(list(cls))
