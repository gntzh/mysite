from collections import Iterable

from django.http import JsonResponse
from functools import wraps
from django.views import decorators


def require_debug(reverse=False):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kw):
            from django.conf import settings
            if settings.DEBUG != reverse:
                return view(*args, **kw)
            return JsonResponse({'code': 403, 'detail': '仅在DEBUG为%s时开放' % bool(not reverse)}, status=403)
        return wrapper
    return decorator


def params(*params):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kw):
            missing = []
            for param in params:
                val = request.GET.get(param)
                if val is None:
                    missing.append(param)
            if missing:
                return JsonResponse({'code': 400, 'detail': '缺少%s参数' % ','.join(missing)}, status=400)
            return view(request, *args, **kw)
        return wrapper
    return decorator
