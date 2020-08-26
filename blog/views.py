from whoosh.qparser import QueryParser
from django.conf import settings
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import LazyObject
from mptt.utils import get_cached_trees
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet, ViewSet

from utils.decorators import params
from libs.rest.mixins import drf as mixins, ListModelMixin, RetrieveModelMixin, ExistsModelMixin
from libs.rest.permissions import isOwnerOrReadOnly
from libs.search.backend import SearchBackend, highlighter
from utils.shortcuts import get_object_or_404
from utils.tools import get_tree


from .search import PostModel
from .models import *
from .utils.serializers import PostSerializer, TagSerializer, CategorySerializer, CommentSerializer, LocalPostSerializer
from .utils.pagination import CommentPagination, Pagination, PostPagination


class PostViewSet(
        ListModelMixin,
        mixins.CreateModelMixin,
        RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    '''
    list:
        获取文章列表
    create:
        添加文章
    retrieve：
        查看文章详情
    update：
        修改文章
    partial_update:
        部分修改文章
    delete:
        删除记录 
    '''
    permission_classes = (isOwnerOrReadOnly('author'), )
    serializer_class = PostSerializer
    queryset = Post.public.select_related(
        'category',  'author', ).prefetch_related('tags')
    pagination_class = PostPagination

    filterset_fields = ('tags', 'category', 'author', )
    search_fields = ('title', 'content', )
    ordering_fields = ('created', 'updated', )
    ordering = '-created'

    many_excluded = ('content', 'is_public', )
    one_excluded = ('excerpt', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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

    @action(detail=True, methods=('post', 'delete'), permission_classes=(IsAuthenticatedOrReadOnly, ))
    def like(self, request, pk):
        post = self.get_object()
        included = set(
            self.many_included or request.query_params.getlist('included')) or None
        excluded = set(request.query_params.getlist(
            'excluded')) | set(self.many_excluded or ())

        if request.method == 'POST':
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)

        return Response({'like_count': post.likes.count()})

    @action(detail=False, methods=('post', ),)
    def from_local(self, request):
        data = request.data.copy()
        id = request.data.get('id')
        categories = data.pop('categories', [])
        category = None
        for level, c in enumerate(categories):
            cate = Category.objects.filter(name__iexact=c, level=level).first()
            if cate is None:
                break
            else:
                category = cate.pk
        data['category'] = category

        tags = []
        for t in data.pop('tags', []):
            tag = Tag.objects.filter(name__iexact=t).first()
            if tag is not None:
                tags.append(tag.pk)
        data.setlist('tags', tags)
        if id is None:
            serializer = LocalPostSerializer(
                data=data, context=self.get_serializer_context())
        else:
            post = get_object_or_404(Post, pk=id)
            serializer = LocalPostSerializer(
                post, data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TagViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        ListModelMixin,
        ExistsModelMixin,
        GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.prefetch_related(
        'posts').annotate(post_count=Count('post'))
    pagination_class = Pagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('id', 'name', )
    search_fields = ('name', )
    ordering_fields = ('post_count', )
    ordering = 'id'

    many_excluded = ('posts',)


class CategoryViewSet(
        mixins.CreateModelMixin,
        RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        ListModelMixin,
        GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = Pagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('id', 'name', 'level',)

    search_fields = ('name',)
    ordering_fields = ('post_count', )
    ordering = 'id'

    many_excluded = ('posts', )
    one_excluded = ('siblings', )

    @action(detail=False)
    def tree(self, request):
        roots = get_cached_trees(
            Category.objects.all())
        return Response(data=[get_tree(root, ('id', 'name', )) for root in roots])

    @action(detail=True, url_path='tree')
    def one_tree(self, request, pk):
        obj = get_object_or_404(self.queryset, pk=pk)
        root = get_cached_trees(obj.get_descendants(include_self=True))
        return Response(data=get_tree(root[0], ('id', 'name', )))


pm = PostModel()


class LazySearchBackend(LazyObject):
    def _setup(self):
        self._wrapped = SearchBackend(pm, settings.INDEX_DIR, pm.indexname)


class LazyQueryParser(LazyObject):
    def _setup(self):
        self._wrapped = QueryParser('text', schema=backend.schema)


backend = LazySearchBackend()
parser = LazyQueryParser()


@api_view(['GET'])
def search(request):
    q = request.GET.get('q')
    if q is not None:
        with backend.index.searcher() as s:
            results = s.search_page(parser.parse(q), 1, pagelen=20, terms=True)
            data = []
            for hit in results:
                data.append({
                    'pk': hit['pk'],
                    'title': highlighter.highlight_hit_whole(hitobj=hit, fieldname='text', text=hit['title']) or hit['title'],
                    'content': highlighter.highlight_hit(hit, 'text', hit['content']) or hit['content'][10:200]
                })
            return Response(data)
    else:
        return Response({'detail': '缺少查询参数q'}, status=400)


class CommentViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    queryset = Comment.objects.all()
    # permission_classes = []
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    filterset_fields = ['post', 'parent', 'reply_to', 'author', ]
    search_fields = ['content', ]
    ordering = '-id'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
