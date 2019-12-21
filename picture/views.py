from rest_framework.viewsets import GenericViewSet

from utils.rest.mixins import drf as mixins

from .models import Album, ThirdPartyImage, Hosting
from .utils.serializers import TPImageSerializer, HostingSerializer, AlbumSerializer
from utils.rest.permissions import isOwnerOrReadOnly
from .utils import filters


class TPImageViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = TPImageSerializer
    queryset = ThirdPartyImage.objects.select_related(
        'owner', 'album').prefetch_related('hostings')
    # pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter, filters.drf_filters.OrderingFilter]
    filterset_fields = ('id', 'description', 'owner', )
    search_fields = ('description', )
    ordering_fields = ['owner', ]
    ordering = '-created'

    # many_excluded = ('posts',)


class HostingViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = HostingSerializer
    queryset = Hosting.objects.select_related('owner', 'image')
    # pagination_class = pagination.Pagination

    filter_backends = (filters.filters.DjangoFilterBackend,
                       filters.drf_filters.OrderingFilter, )
    filterset_fields = ('id', 'owner', )
    ordering_fields = ('owner', )
    ordering = '-id'


class AlbumViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    permission_classes = (isOwnerOrReadOnly(), )
    serializer_class = AlbumSerializer
    queryset = Album.objects.select_related('owner')
    # pagination_class = pagination.Pagination

    filter_backends = [filters.filters.DjangoFilterBackend,
                       filters.drf_filters.SearchFilter, filters.drf_filters.OrderingFilter]
    filterset_fields = ('id', 'name', 'owner', )
    search_fields = ('name', )
    ordering_fields = ('owner', )
    ordering = '-created'
