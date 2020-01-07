from rest_framework.validators import ValidationError, qs_exists
from ..models import Post, Tag, Category


def createOrUpdate(data):
    id = data.get('pk', None)
    if id is None:
        id = data.get('id', None)
    return id


def get_data(id, data, model, *fields):
    res = {}
    for f in fields:
        try:
            res[f] = data[f]
        except KeyError as e:
            obj = model.objects.get(pk=id)
            res[f] = obj.f


def uniqueCate(data):
    id = createOrUpdate(data)
    queryset = Category.objects.filter(
        name=data['name'], owner=data['owner'], parent__isnull=True)
    if(id):
        queryset.exclude(id=data.id)
    if data['parent'] is None and qs_exists(queryset):
        raise ValidationError('字段 owner, name, parent 必须能构成唯一集合。')
    return data
