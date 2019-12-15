from rest_framework import mixins as drf
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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


class ExistsModelMixin:
    """
    由查询条件判断实例是否存在
    存在返回True, 不存在就创建(POST)
    """
    @action(detail=False, methods=['GET', 'POST', ], url_path='exists', url_name='exists', permission_classes=[IsAuthenticatedOrReadOnly, ])
    def exists(self, request, *args, **kwargs):
        """
        由查询条件判断实例是否存在
        存在返回True, 不存在就创建(POST)
        """
        exists = self.filter_queryset(self.get_queryset()).exists()
        if request.method == 'GET':
            return drf.Response({'exists': exists})
        else:
            if exists:
                return drf.Response({'exists': True})
            return self.create(request, *args, **kwargs)
