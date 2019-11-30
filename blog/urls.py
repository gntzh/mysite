from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "blog"
router = routers.DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"tags", views.TagViewSet)
# router.register(r"one_man_posts", views.OneManPostViewSet)
# owner_articles
urlpatterns = [
    path(r"", include(router.urls)),
    path("one_man_posts/<int:pk>/",
         views.OneManPostList.as_view({"get": "list"})),
    path("one_man_tags/<int:pk>/",
         views.OneManTagList.as_view({"get": "list"})),
    path("one_man_categories/<int:pk>/",
         views.OneManCategoryList.as_view({"get": "list"})),
]
