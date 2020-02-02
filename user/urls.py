from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r'auth', views.ThirdPartyLogin, 'auth')

urlpatterns = [
    path(r'', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("verify_email/", views.VerifyEmailViewSet.as_view({"post": "sendVerifyEmail",
                                                            "get": "checkVerifyEmailUrl"}),
         name="verify_email"),
    # path("users/", views.UserViewSet.as_view({"get": "list", "post": "create"})),
    # path("users/<int:pk>/", views.UserViewSet.as_view({"delete": "destroy", "get": "retrieve"}),),
]
