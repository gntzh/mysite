from rest_framework import relations


class PrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):

    def __init__(self, method=None, **kw):
        self.method = method
        super().__init__(**kw)

    def use_pk_only_optimization(self):
        if self.pk_field is not None:
            return False
        return True

    def to_representation(self, value):
        if self.method is not None:
            return self.method(value)
        if self.pk_field is not None:
            return self.pk_field.to_representation(value)  # default: value.pk
        return value.pk

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]
        return {
            item.pk: self.display_value(item) for item in queryset
        }
