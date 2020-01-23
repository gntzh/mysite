from django.urls import path, include
from rest_framework import routers
from .views import BlogCommentViewset

app_name = 'comment'
router = routers.DefaultRouter()
router.register(r'blog_comments', BlogCommentViewset)

urlpatterns = [
    path(r'', include(router.urls)),
]
