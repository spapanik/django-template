from datetime import datetime
from typing import List

from django.db import models

from lib.datetime import now


class BaseManager(models.Manager):
    def bulk_create(self, objs, *args, **kwargs):
        dt = now()
        for obj in objs:
            obj.updated_at = dt
            obj.created_at = dt
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, fields: List[str], *args, **kwargs):
        dt = now()
        for obj in objs:
            obj.updated_at = dt
        if "updated_at" not in fields:
            fields += ["updated_at"]
        return super().bulk_update(objs, fields, *args, **kwargs)


def queryset_as_manager(queryset_class):
    return BaseManager.from_queryset(queryset_class)()


class ForeignKey(models.ForeignKey):
    def __init__(
        self,
        to,
        on_delete=models.CASCADE,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field=None,
        db_constraint=True,
        **kwargs,
    ):
        super().__init__(
            to,
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs,
        )


class OneToOneField(models.OneToOneField):
    def __init__(self, to, on_delete=models.CASCADE, to_field=None, **kwargs):
        super().__init__(to, on_delete=on_delete, to_field=to_field, **kwargs)


class BaseQuerySet(models.QuerySet):
    def flat_values(self, key: str) -> models.QuerySet:
        return self.values_list(key, flat=True)

    def random(self):
        return self.order_by("?").first()


class BaseModel(models.Model):
    created_at: datetime = models.DateTimeField(default=now, editable=False)
    updated_at: datetime = models.DateTimeField(default=now, editable=False)

    objects: BaseManager = queryset_as_manager(BaseQuerySet)

    class Meta:
        abstract = True
