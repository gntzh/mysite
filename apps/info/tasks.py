from celery import task
from django.utils import timezone
from .utils.dingtalk import send_info
from . import bots


@task
def tody_in_history():
    now = timezone.localdate()
    send_info({
        "feedCard": {
            "links": bots.thisday.lssdjt(now.month, now.day),
        },
        "msgtype": "feedCard"
    })
