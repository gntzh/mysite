from rest_framework.validators import ValidationError, UniqueTogetherValidator, qs_exists


class RelatedToOwnValidator:
    def __init__(self, m2m=False, from_owner_field='owner', to_owner_field='owner'):
        self.m2m = m2m
        self.from_owner_field = from_owner_field
        self.to_owner_field = to_owner_field

    requires_context = True

    def __call__(self, data, serializer_field):
        instance = getattr(serializer_field.parent, 'instance', None)
        from_owner = getattr(instance, self.from_owner_field)
        if self.m2m:
            for i in data:
                if getattr(i, self.to_owner_field) != from_owner:
                    raise ValidationError('不允许关联他人的%s' %
                                          serializer_field.source_attrs[-1])
        else:
            if getattr(data, self.to_owner_field) != from_owner:
                raise ValidationError('不允许关联他人的%s' %
                                      serializer_field.source_attrs[-1])
        return data


class M2MNumValidator:
    def __init__(self, max_num=None, min_num=None):
        self.max_num = max_num
        self.min_num = min_num

    requires_context = True

    def __call__(self, data, serializer_field):
        num = len(data)
        if self.min_num is not None:
            if num < self.min_num:
                raise ValidationError('%s关联不得少于%d个' % (
                    serializer_field.source_attrs[-1], self.min_num))
        if self.max_num is not None:
            if num > self.max_num:
                raise ValidationError('%s关联不得多于%d个' % (
                    serializer_field.source_attrs[-1], self.max_num))
        return data
