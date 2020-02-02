from django.http import JsonResponse
from functools import wraps


def require_debug(reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            from django.conf import settings
            if settings.DEBUG != reverse:
                return func(*args, **kw)
            return JsonResponse({'code': 403, 'detail': '仅在DEBUG为%s时开放' % bool(not reverse)}, status=403)
        return wrapper
    return decorator
