# settings.py
import os

# Default config between dev and prd
# export SITE_ENV =  'production'
if os.environ.get('SITE_ENV', None):
    from .config.production import *
else:
    from .config.develop import *
