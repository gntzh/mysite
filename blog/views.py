from haystack.query import EmptySearchQuerySet, SearchQuerySet
from django.db.models import Count
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet, ViewSet

from utils.rest.mixins import drf as mixins, ListModelMixin, RetrieveModelMixin, ExistsModelMixin
from utils.rest.permissions import isOwnerOrReadOnly
from utils.shortcuts import get_object_or_404

from .models import Post, Tag, Category
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
    queryset = Post.public.select_related(
        'category', 'category__parent', 'author', ).prefetch_related('tags')
    pagination_class = pagination.PostPagination

    filterset_fields = ('tags', 'category', 'author', )
    search_fields = ('title', 'content', )
    ordering_fields = ('created', 'updated', )
    ordering = '-created'

    many_excluded = ('content', 'is_public', )
    one_excluded = ('excerpt', )

    @action(detail=True, url_path='similar', url_name='similar_post')
    def similar(self, request, pk):
        post = get_object_or_404(Post.public, pk=pk)
        post_tags_ids = post.tags.values_list('id')
        similar_posts = Post.public.filter(
            tags__in=post_tags_ids).exclude(pk=post.id)
        queryset = similar_posts.annotate(same_tags_count=Count(
            'tags')).order_by('-same_tags_count', '-created')[:4]
        serializer = self.get_serializer(
            queryset, many=True, excluded=('is_public',))
        return Response(serializer.data)


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
        'owner').prefetch_related('posts').annotate(post_count=Count('post'))
    pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter, filters.drf_filters.OrderingFilter]
    filterset_fields = ('id', 'name', 'owner', )
    search_fields = ('name', )
    ordering_fields = ('post_count', )
    ordering = 'id'

    many_excluded = ('posts',)


defer = ["last_login",
         "is_superuser",
         "first_name",
         "last_name",
         "is_staff",
         "date_joined",
         "nickname",
         "avatar",
         "phone",
         "email",
         "is_active",
         "email_is_active",
         "created",
         "sign",
         "password", ]


class CategoryViewSet(
        mixins.CreateModelMixin,
        RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        ListModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related('owner', 'parent').prefetch_related(
        'posts', 'children', ).defer(*('owner__' + i for i in defer)).annotate(post_count=Count('post'))
    pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter,
                       filters.drf_filters.OrderingFilter]
    filterset_class = filters.CategoryFilter
    search_fields = ('name',)
    ordering_fields = ('post_count', )
    ordering = 'id'

    many_excluded = ('posts', 'children', 'siblings', )
    one_excluded = ('siblings', )

    @action(detail=True, url_path='display', url_name='display', permission_classes=[])
    def display(self, request, *args, **kwargs):
        '''
        用于前端树形控件展示分类
        '''
        included = ('name',)
        try:
            cates = CategorySerializer(self.queryset.filter(
                parent=kwargs['pk']), included=('id', 'name', 'is_leaf'), many=True)
            posts = PostSerializer(Post.objects.filter(
                category=kwargs['pk']), included=('id', 'title', ), many=True)
        except (TypeError, ValueError):
            raise Http404
        return Response(cates.data + posts.data)

# TODO 搜索高亮
@api_view(['GET'])
def search(request, load_all=True,  searchqueryset=None):
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        query = request.GET.get('q')
        print(query)
        if searchqueryset is None:
            searchqueryset = SearchQuerySet()
        sqs = searchqueryset.models(Post).auto_query(request.GET.get('q'))
        sqs = sqs.load_all()
        results = sqs.highlight()
    else:
        raise Http404('缺少查询参数q')

    # print(results)
    # print(dir(results))
    # print(results[0].title, results[0].pk, results[0].author)
    # se = PostSerializer(results, many=True, included=('title', ))
    # print(se.data)
    return Response(data=[i.highlighted['text'][0] for i in results])
