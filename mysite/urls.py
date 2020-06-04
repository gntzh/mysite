"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from blog.utils.feeds import PostFeed, LatestPostsFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-user/', include('user.urls')),
    path('api-blog/', include('blog.urls')),
    path('api-picture/', include('picture.urls')),
    path('api-comment/', include('comment.urls')),
    path('chat/', include('chat.urls')),
    path('rss/blog/', LatestPostsFeed()),
    path('rss/u/<int:user_id>/blog/', PostFeed()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


schema_view = get_schema_view(
    openapi.Info(
        title="MySite Open API",
        default_version='v0.1.0',
        description="MySite开放API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shoor@foxmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
]
