# settings.py
import os

# Default config between dev and prd
# export DJ_ENV =  'production'
if os.environ.get('DJ_ENV', None):
    from .config.production import *
else:
    from .config.develop import *
