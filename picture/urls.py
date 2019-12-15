from django.urls import path, include
from rest_framework import routers
from .views import TPImageViewSet, HostingViewSet, AlbumViewSet

app_name = 'picture'
router = routers.DefaultRouter()
router.register(r'tp_images', TPImageViewSet)
router.register(r'hostings', HostingViewSet)
router.register(r'albums', AlbumViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
