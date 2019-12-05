# settings.py
import os

# Default config between dev and prd
# export SITE_ENV =  'production'
ENV = os.environ.get('SITE_ENV', None)
if ENV == "production":
    from .config.prod import *
elif ENV == "development":
    from .config.dev import *
else:
    from .config.dev import *
