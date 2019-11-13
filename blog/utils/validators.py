from rest_framework.serializers import ValidationError, UniqueTogetherValidator
from .. import models


def validateParent(data):
    print(data)
    parent = data.parent
    id = data.id
    if parent is None:
        return data
    if parent.id == id:
        raise ValidationError("不允许关联分类本身")
    if parent.owner != data.owner:
        raise ValidationError("不允许关联他人的分类")
    return data