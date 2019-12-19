from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CategoryViewSet, TagViewSet


app_name = 'blog'
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
