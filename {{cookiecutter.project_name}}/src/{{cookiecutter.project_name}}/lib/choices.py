from secrets import choice

from django.db import models


class Choices(models.TextChoices):
    @classmethod
    def random(cls):
        return choice(list(cls))
