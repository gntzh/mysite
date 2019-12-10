from rest_framework.validators import ValidationError, UniqueTogetherValidator, qs_exists
from .. import models


def createOrUpdate(data):
    id = data.get('pk', None)
    if(id):
        id = data.get('id', None)
    return id


def validateParent(data):
    parent = data['parent']
    id = createOrUpdate(data)
    if parent is None:
        return data
    if parent.id == id:
        raise ValidationError("不允许关联分类本身")
    if parent.owner != data['owner']:
        raise ValidationError("不允许关联他人的分类")
    return data


def uniqueCate(data):
    id = createOrUpdate(data)
    queryset = models.Category.objects.filter(
        name=data['name'], owner=data['owner'], parent__isnull=True)
    if(id):
        queryset.exclude(id=data.id)
    if data['parent'] is None and qs_exists(queryset):
        raise ValidationError("字段 owner, name, parent 必须能构成唯一集合。")
    return data
