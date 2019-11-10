from . import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
# django rest framework
from rest_framework.views import APIView, Response, Request
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import decorators
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import mixins
import django_filters.rest_framework

from rest_framework import filters

from .utils.serializers import PostSerializer, TagSerializer, CategorySerializer
from .utils import pagination, permissions

User = get_user_model()


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    serializer_class = PostSerializer
    queryset = models.Post.objects.filter(is_public=True)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,]
    filterset_fields = ["tags", "category"]
    search_fields = ['title', 'content']
    ordering_fields = ["created_time", "modified_time"]
    pagination_class = pagination.PostPagination


class TagViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    serializer_class = TagSerializer
    queryset = models.Tag.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,
                       ]
    filterset_fields = ["id", "name"]
    search_fields = ['name', 'owner']
    ordering_fields = ["owner"]
    pagination_class = pagination.Pagination


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    serializer_class = CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,
                       ]
    filterset_fields = ["id", "name"]
    search_fields = ['name', 'owner']
    ordering_fields = ["-post_num"]
    pagination_class = pagination.Pagination


class OneManPostList(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.UserExist, ]
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,
                       ]
    filterset_fields = ["tags", "category"]
    search_fields = ['title', 'content']
    ordering_fields = ["created_time", "modified_time"]
    pagination_class = pagination.PostPagination

    def get_queryset(self):
        pk = int(self.request.path.strip("/").split("/")[-1])
        if self.request.user and self.request.user.is_authenticated:
            return models.Post.objects.filter(author=pk)
        return models.Post.objects.filter(author=pk, is_public=True)


class OneManTagList(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.UserExist, ]
    serializer_class = TagSerializer
    pagination_class = pagination.Pagination

    def get_queryset(self):
        pk = int(self.request.path.strip("/").split("/")[-1])
        return models.Tag.objects.filter(owner=pk)


class OneManCategoryList(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.UserExist, ]
    pagination_class = pagination.Pagination

    def get_queryset(self):
        pk = int(self.request.path.strip("/").split("/")[-1])
        return models.Category.objects.filter(owner=pk)
