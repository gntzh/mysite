from .production import *
# 开发环境
SECRET_KEY = 'd+h0io02_a8=g#v9&4adwkbbtkn!usqd3fhn9xf(g7a-ln32al'
DEBUG = True

INTERNAL_IPS = ['127.0.0.1', ]

SITE_HOST = 'http://127.0.0.1:8000'

## django-cors-headers
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
)