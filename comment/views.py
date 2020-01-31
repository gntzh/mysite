from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from blog.models import Post
from .models import RootComment, ChildComment
# from .utils.filters import CommentFilter
from .utils.serializers import PostRootCommentSerializer, PostChildCommentSerializer


class PostRootCommentViewset(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    '''博文评论
    '''
    permission_classes = ()
    queryset = RootComment.objects.filter(
        content_type=ContentType.objects.get_for_model(Post))
    serializer_class = PostRootCommentSerializer
    # filter_class = CommentFilter
    search_fields = ('name',)
    filterset_fields = ('id', 'owner', 'object_id', )
    ordering_fields = ('created',)
    ordering = '-created'

    @action(detail=True)
    def child_comments(self, request, pk):
        queryset = ChildComment.objects.filter(root_comment=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostChildCommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostChildCommentSerializer(queryset, many=True)
        return Response(serializer.data)
