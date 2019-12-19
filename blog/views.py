from .models import Post, Tag, Category
# django rest framework
# from rest_framework.views import APIView, Response, Request
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.reverse import reverse

from utils.rest.mixins import drf as mixins, ListModelMixin, RetrieveModelMixin, ExistsModelMixin
from utils.rest.permissions import isOwnerOrReadOnly

from .utils.serializers import PostSerializer, TagSerializer, CategorySerializer
from .utils import pagination, filters


class PostViewSet(
        ListModelMixin,
        mixins.CreateModelMixin,
        RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly('author'), )
    serializer_class = PostSerializer
    queryset = Post.objects.select_related(
        'category', 'category__parent', 'author', ).prefetch_related('tags').filter(is_public=True)
    pagination_class = pagination.PostPagination

    filterset_fields = ('tags', 'category', )
    search_fields = ('title', 'content', )
    ordering_fields = ('created', 'updated', )
    ordering = '-created'

    many_excluded = ('content', 'is_public', )
    one_excluded = ('excerpt', )


class TagViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        ListModelMixin,
        ExistsModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = TagSerializer
    queryset = Tag.objects.select_related(
        'owner').prefetch_related('posts')
    pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter, filters.drf_filters.OrderingFilter]
    filterset_fields = ('id', 'name', 'owner', )
    search_fields = ('name', )
    ordering_fields = ('owner', )
    ordering = 'id'

    many_excluded = ('posts',)


class CategoryViewSet(
        mixins.CreateModelMixin,
        RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        ListModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related(
        'owner', 'parent').prefetch_related('posts', 'children')
    pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter,
                       filters.drf_filters.OrderingFilter]
    filterset_class = filters.CategoryFilter
    search_fields = ('name',)
    ordering_fields = ('posts', 'post_num')
    ordering = 'id'

    many_excluded = ('posts', 'children')
    one_excluded = ('is_leaf',)
