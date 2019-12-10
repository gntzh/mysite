from rest_framework import mixins as drf


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        excluded = getattr(self, 'one_excluded', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, excluded=excluded)
        return drf.Response(serializer.data)



class ListModelMixin:
    """
    List a queryset.
    判断是否
    """
    def list(self, request, *args, **kwargs):
        excluded = getattr(self, 'many_excluded', None)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, excluded=excluded)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, excluded=excluded)
        return drf.Response(serializer.data)

