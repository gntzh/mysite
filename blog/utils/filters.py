from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .. import models


class CategoryFilter(filters.FilterSet):
    top = filters.BooleanFilter('parent', 'isnull', label='是否顶级分类')

    class Meta:
        model = models.Category
        fields = ('top', 'id', 'name', 'owner', 'parent', )
