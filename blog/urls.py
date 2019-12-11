from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'blog'
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('one_man_posts/<int:pk>/',
         views.OneManPostList.as_view({'get': 'list'})),
]
