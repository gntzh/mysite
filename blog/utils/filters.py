from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from ..models import Category


class CategoryFilter(filters.FilterSet):
    is_root = filters.BooleanFilter('parent', 'isnull', label='是否一级分类')

    class Meta:
        model = Category
        fields = ('is_root', 'id', 'name', 'owner', 'parent', )
