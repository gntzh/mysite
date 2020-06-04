import os.path
from django.urls import path, include, re_path, reverse
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .views import PostViewSet, CategoryViewSet, TagViewSet, CommentViewSet, search


app_name = 'blog'
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'search/', search),
]


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(
            schema.basePath, reverse(app_name + ':api-root'))
        return schema


schema_view = get_schema_view(
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
    generator_class=SchemaGenerator,
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]
