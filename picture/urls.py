from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'picture'
router = routers.DefaultRouter()
router.register(r'tp_images', views.TPImageViewSet)
router.register(r'hostings', views.HostingViewSet)
# router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
