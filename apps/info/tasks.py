import re
import time
from celery import task
from django.utils import timezone
from redis import StrictRedis

from .utils import redis_conn_pool
from .utils.dingtalk import send_info
from .bots import thisday, weibo_api


@task
def test_task():
    print('I am here..........')
    time.sleep(3)
    print('Completed!!!!!!!!!!')


@task
def tody_in_history():
    now = timezone.localdate()
    send_info({
        "feedCard": {
            "links": thisday.lssdjt(now.month, now.day),
        },
        "msgtype": "feedCard"
    })


@task
def weibo_home_line():
    redis_client = StrictRedis(connection_pool=redis_conn_pool)
    since_id = redis_client.get('info_app_weibo_api_since_id')
    if since_id is None:
        posts = weibo_api.home_line(count=1)
    else:
        posts = weibo_api.home_line(since_id=since_id)
    if posts:
        redis_client.set('info_app_weibo_api_since_id', posts[0]['idstr'])
        for i in posts:
            p = {'btnOrientation': '0',
                 'singleTitle': '阅读全文',
                 'singleURL': f'https://m.weibo.cn/status/{i["idstr"]}?', }
            p['title'] = i['user']['screen_name'] + '：' + i['text'][:16]
            t = re.sub(
                r'#(.+?)#', '[\g<0>](https://m.weibo.cn/search?containerid=231522type=1&t=10&q=\g<1>&extparam=\g<1>)', i['text'])
            p['text'] = re.sub(
                r'@(.+?) ', '[@\g<1>](https://m.weibo.cn/n/\g<1>) ', t)

            send_info({
                "actionCard": p,
                "msgtype": "actionCard",
            })
