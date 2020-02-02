from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework.views import Response, status
import requests
from urllib.parse import urlencode

from utils.jwt import get_tokens_for_user
from utils.rest.mixins import ListModelMixin, RetrieveModelMixin
from django.shortcuts import redirect
from .models import OUser
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


def check_state(state, expected_type):
    '''state检查
    state约定:identifier_type.redirect.random_value
    '''
    try:
        identifier_type, redirect, random_value = state.split('.')
    except (ValueError, AttributeError):
        return False
    if identifier_type != expected_type:
        return False
    return True


class ThirdPartyLogin(ViewSet):

    @action(detail=False)
    def github(self, request):
        callback = request.query_params.get(
            'callback', reverse('auth-github-callback', request=request))
        state = request.query_params.get('state', settings.FRONT_HOST)
        if not check_state(state, 'gh'):
            return Response({'detail': '无效的state'}, status=status.HTTP_404_NOT_FOUND)

        url = 'https://github.com/login/oauth/authorize'+'?' + \
            urlencode({'client_id': '39a0b30fd1c6433d43e1',
                       'redirect_uri': callback,
                       'state': state,
                       })
        return redirect(url)

    @action(detail=False)
    def github_callback(self, request):
        code = request.query_params.get('code')
        if code is None:
            return Response({'detail': '缺失查询参数code'}, status=status.HTTP_404_NOT_FOUND)

        url = 'https://github.com/login/oauth/access_token'
        params = {'code': code,
                  'client_id': settings.GITHUB_APP_ID,
                  'client_secret': settings.GITHUB_APP_SECRET,
                  }
        res = requests.get(url, params=params, headers={
            'accept': 'application/json'})

        if res.status_code == 200 and not res.json().get('error', False):
            res = requests.get('https://api.github.com/user', headers={
                               'authorization': 'bearer ' + res.json().get('access_token')})
            info = res.json()
            ouser = OUser.objects.filter(
                identifier=info['node_id'], identity_type='gh')
            if ouser.exists():
                u = ouser[0].user
            else:
                u = User.objects.create_user(username='gh_' + info['node_id'])
                OUser(identifier=info['node_id'],
                      identity_type='gh', user=u).save()
            tokens = get_tokens_for_user(u)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({'detail': '无效code'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def github_userinfo_callback(self, req):
        print(req, req.query_params, dir(req))
        return Response({'token': 'hhhhh'}, status=200)
