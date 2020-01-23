from django_filters import rest_framework as dj_filters
from rest_framework import filters as drf_filters
from ..models import Comment


class CommentFilter(dj_filters.FilterSet):
    is_root = dj_filters.BooleanFilter('parent', 'isnull', label='是否一级评论')

    class Meta:
        model = Comment
        fields = ('is_root', 'id', 'parent', 'object_id')
