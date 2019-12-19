from rest_framework.validators import ValidationError, qs_exists
from ..models import Post, Tag, Category


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
        raise ValidationError('不允许关联分类本身')
    return data


def uniqueCate(data):
    id = createOrUpdate(data)
    queryset = Category.objects.filter(
        name=data['name'], owner=data['owner'], parent__isnull=True)
    if(id):
        queryset.exclude(id=data.id)
    if data['parent'] is None and qs_exists(queryset):
        raise ValidationError('字段 owner, name, parent 必须能构成唯一集合。')
    return data
