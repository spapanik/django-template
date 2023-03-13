from collections.abc import Iterable
from datetime import datetime
from typing import Any

from django.db import models

from {{cookiecutter.project_name}}.lib.date_utils import now


class BaseManager(models.Manager):
    def bulk_create(self, objs: Iterable[Any], *args, **kwargs):
        dt = now()
        for obj in objs:
            obj.updated_at = dt
            obj.created_at = dt
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs: Iterable[Any], fields: list[str], *args, **kwargs):
        dt = now()
        for obj in objs:
            obj.updated_at = dt
        if "updated_at" not in fields:
            fields += ["updated_at"]
        return super().bulk_update(objs, fields, *args, **kwargs)


def queryset_as_manager(queryset_class):
    return BaseManager.from_queryset(queryset_class)()


class ForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs.setdefault("on_delete", models.CASCADE)
        super().__init__(to, **kwargs)


class OneToOneField(models.OneToOneField):
    def __init__(self, to, **kwargs):
        kwargs.setdefault("on_delete", models.CASCADE)
        super().__init__(to, **kwargs)


class BaseQuerySet(models.QuerySet):
    def flat_values(self, key: str) -> models.QuerySet:
        return self.values_list(key, flat=True)

    def random(self):
        return self.order_by("?").first()

    def update(self, **kwargs):
        kwargs.setdefault("updated_at", now())
        return super().update(**kwargs)


class BaseModel(models.Model):
    created_at: datetime = models.DateTimeField(default=now, editable=False)
    updated_at: datetime = models.DateTimeField(default=now, editable=False)

    objects: BaseManager = queryset_as_manager(BaseQuerySet)

    def save(self, *args, **kwargs) -> None:
        self.updated_at = now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
