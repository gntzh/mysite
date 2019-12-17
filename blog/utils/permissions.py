from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()

OWNER_METHODS = ['PUT', 'PATCH', 'DELETE']


class UserExist(BasePermission):
    def has_permission(self, request, view):
        pk = request.path.strip('/').split('/')[-1]
        pk = int(pk)
        print(pk)
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            self.message = '用户不存在'
            return False
        return True
