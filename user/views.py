from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.views import Response, status
from django.contrib.auth import get_user_model

from utils.rest.mixins import ListModelMixin, RetrieveModelMixin
from . utils import verify, serializers, permissions

User = get_user_model()


class VerifyEmailViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def sendVerifyEmail(self, request):
        data = {}
        user = request.user
        if not user.email:
            data['message'] = '用户未添加邮箱'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        verify_url = verify.generateVerifyEmailUrl(user)
        # verify.sendVerifyEmail.delay(user, verify_url)
        verify.sendVerifyEmail(user, verify_url)
        data['message'] = '已发送邮件'
        return Response(data, status=status.HTTP_200_OK)

    def checkVerifyEmailUrl(self, request):
        data = {}
        key = request.GET.get('key', None)
        if not key:
            data['message'] = '无效的链接, 缺失key'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        is_success, user = verify.checkVerifyEmailUrl(key)
        if is_success:
            user.email_is_active = True
            user.save()
            data['message'] = '验证成功'
            return Response(data)
        data['message'] = '验证失败'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ListModelMixin,
                  mixins.CreateModelMixin,
                  RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    ordering = 'id'

    one_included = many_included = (
        'id', 'username', 'nickname', 'avatar', 'sign')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, included=self.one_included)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(['post', ], detail=True,
            url_path='change_pwd', url_name='change_pwd',
            permission_classes=[permissions.IsOwnerOrAdmin])
    def changePassword(self, request, pk=None):
        return Response(['修改成功'])
