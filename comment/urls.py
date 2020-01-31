from django.urls import path, include
from rest_framework import routers
from .views import PostRootCommentViewset, PostChildCommentViewset

app_name = 'comment'
router = routers.DefaultRouter()
router.register(r'post_root_comments', PostRootCommentViewset)
router.register(r'post_child_comments', PostChildCommentViewset)

urlpatterns = [
    path(r'', include(router.urls)),
]
