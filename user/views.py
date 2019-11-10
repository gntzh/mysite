from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.views import Response, status
from django.contrib.auth import get_user_model

from . utils import verify, serializers, permissions

User = get_user_model()


class VerifyEmailViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def sendVerifyEmail(self, request):
        data = {}
        user = request.user
        if not user.email:
            data["message"] = "用户未添加邮箱"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        verify_url = verify.generateVerifyEmailUrl(user)
        # verify.sendVerifyEmail.delay(user, verify_url)
        verify.sendVerifyEmail(user, verify_url)
        data["message"] = "已发送邮件"
        return Response(data, status=status.HTTP_200_OK)

    def checkVerifyEmailUrl(self, request):
        data = {}
        key = request.GET.get("key", None)
        if not key:
            data["message"] = "无效的链接, 缺失key"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        is_success, user = verify.checkVerifyEmailUrl(key)
        if is_success:
            user.email_is_active = True
            user.save()
            data["message"] = "验证成功"
            return Response(data)
        data["message"] = "验证失败"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAdminUser, ]
        elif self.action == "create":
            permission_classes = []
        elif self.action in ("update", "partial_update", "destroy", ):
            permission_classes = [permissions.IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("update", "partial_update", ):
            return serializers.UserUpdateSerializer
        return super().get_serializer_class()

    @action(['post', ], detail=True,
            url_path='change-pwd', url_name='change_pwd',
            permission_classes=[permissions.IsOwnerOrAdmin])
    def changePassword(self, request, pk=None):
        return Response(["修改成功"])

