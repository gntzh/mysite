from django.urls import path, include
from rest_framework import routers
from .views import PostRootCommentViewset

app_name = 'comment'
router = routers.DefaultRouter()
router.register(r'post_root_comments', PostRootCommentViewset)

urlpatterns = [
    path(r'', include(router.urls)),
]
