from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class TimeMixin:
    created_at = models.DateTimeField("创建时间", default=timezone.now)
    updated_at = models.DateTimeField("修改时间")


class LogicallyDeleteQuerySet(QuerySet):
    def logically_delete(self):
        self.update(is_deleted=True)


class LogicalManager(models.Manager):
    _queryset_class = LogicallyDeleteQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(id_deleted=False)


class LogicallyDeleteMixin:
    is_deleted = models.BooleanField("逻辑删除", default=False)
    deleted_at = models.DateTimeField("删除时间", null=True, default=None)

    logical_objects = LogicalManager()

    def logically_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'is_deleted'])
