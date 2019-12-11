from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()

OWNER_METHODS = ['PUT', 'PATCH', 'DELETE']

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return IsAuthenticated().has_permission(request, view)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            user = obj.author
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user == obj.author
            )
        except:
            try:
                user = obj.owner
                return bool(
                    request.user and
                    request.user.is_authenticated and
                    request.user == obj.owner
                )
            except:
                return False


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
