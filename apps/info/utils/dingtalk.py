import hmac
import hashlib
import base64
from django.conf import settings
from django.utils import timezone
import requests
from ..bots.thisday import baidu_calendar
from ..utils import timestamp


def send_info(info):
    stamp = timestamp()
    secret = settings.DINGTALK_SECRET
    string = f'{stamp}\n{secret}'
    hmac_sign = hmac.new(
        secret.encode('utf-8'), string.encode('utf-8'), digestmod=hashlib.sha256).digest()
    params = {
        'access_token': settings.DINGTALK_ACCESS_TOKEN,
        'timestamp': stamp,
        'sign': base64.b64encode(hmac_sign)
    }
    webhook = 'https://oapi.dingtalk.com/robot/send'
    res = requests.post(webhook, params=params, json=info)
    return res.json().get('errmsg', 'success')
