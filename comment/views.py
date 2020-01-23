from django.contrib.contenttypes.models import ContentType
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from blog.models import Post
from .models import Comment
from .utils.filters import CommentFilter
from .utils.serializers import BlogCommentSerializer


class BlogCommentViewset(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = ()
    queryset = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Post))
    serializer_class = BlogCommentSerializer
    filter_class = CommentFilter
    search_fields = ('name',)
    filterset_fields = ('id', 'owner', )
    ordering_fields = ('created',)
    ordering = '-created'
