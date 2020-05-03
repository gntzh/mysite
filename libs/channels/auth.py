import re
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    """
    Attempts to find and return a user using the given validated token.
    """
    try:
        user = User.objects.get(**{jwt_settings.USER_ID_FIELD: user_id})
    except User.DoesNotExist:
        return AnonymousUser()
    # if not user.is_active:
    #     return AnonymousUser()
    return user


class JWTAuthMiddleware(BaseMiddleware):

    def populate_scope(self, scope):
        scope['user_id'] = self.authenticate(scope)
        scope["user"] = UserLazyObject()
        return self.inner(scope)

    async def resolve_scope(self, scope):
        # 异步机制不明, 不使用UserLazyObject, 造成Consumer处获取不到user
        scope['user']._wrapped = await get_user(scope.pop('user_id'))


    def authenticate(self, scope):
        header = self.get_header(scope)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        for AuthToken in jwt_settings.AUTH_TOKEN_CLASSES:
            try:
                validated_token = AuthToken(raw_token)
                break
            except TokenError:
                return None
        try:
            return validated_token[jwt_settings.USER_ID_CLAIM]
        except KeyError:
            return None

    def get_header(self, scope):
        """
        Extracts the header containing the JSON web token from the given
        scope.
        """
        if b'authorization' in scope['headers']:
            return scope['headers'][b'authorization'].decode()

        m = re.search(
            r'k=(?P<token>[A-Za-z]+?%20[A-Za-z0-9-_\.]+)&?', scope['query_string'].decode())
        if m is not None:
            return m.group('token').replace('%20', ' ', 1)
        return None

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()
        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None
        if parts[0] not in jwt_settings.AUTH_HEADER_TYPES:
            # Assume the header does not contain a JSON web token
            return None
        if len(parts) != 2:
            return None
        return parts[1]


def JWTAuthMiddlewareStack(inner): return CookieMiddleware(
    SessionMiddleware(JWTAuthMiddleware(inner))
)
