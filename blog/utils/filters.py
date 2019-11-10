from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
filters.FilterSet
drf_filters.BaseFilterBackend
class ArticleOwnerFilter(filter.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)