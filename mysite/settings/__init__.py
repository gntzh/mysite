# settings.py
import os
import configparser
from pathlib import Path

mode = os.environ.get('SITE_MODE', 'dev')
base = Path(__file__).resolve().parent.parent.parent

conf = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation())
conf.read(base / '.env')
env = conf[mode if conf.has_section(mode) else 'dev']

exec('from .%s import *' % env.get('settings', 'dev'))

SECRET_KEY = env['SECRET_KEY']

GITHUB_APP_KEY = env['GITHUB_APP_KEY']
GITHUB_APP_SECRET = env['GITHUB_APP_SECRET']

DINGTALK_ACCESS_TOKEN = env['DINGTALK_ACCESS_TOKEN']
DINGTALK_SECRET = env['DINGTALK_SECRET']

EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']
DEFAULT_EMAIL_FROM = env['DEFAULT_EMAIL_FROM']

WEIBO_ACCESS_TOKEN = env['WEIBO_ACCESS_TOKEN']
