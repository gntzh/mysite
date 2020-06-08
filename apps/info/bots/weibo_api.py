import re
from django.conf import settings
from redis import StrictRedis
import requests
from . import exceptions
from ..utils import redis_conn_pool


def get_since_id():

    since_id = redis_client.get('info_app_weibo_home_line_since_id')
    if since_id is not None:
        return since_id


def home_line(since_id=None, count=None):
    params = {
        'access_token': settings.WEIBO_ACCESS_TOKEN,
        'count': count or 100,
        'trim_user': 0,  # TODO 改为1, 用户名从数据库获取
        'feature': 1,  # TODO 改为0, 针对每条信息进行判断
    }
    if since_id is not None:
        params['since_id'] = since_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    url = 'https://api.weibo.com/2/statuses/home_timeline.json'
    res = requests.get(url, params=params, headers=headers)
    data = res.json().get('statuses')
    if data is None:
        raise exceptions.APIException('微博home_timeline接口异常')
    return data
