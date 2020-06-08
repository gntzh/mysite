import time
from faker import Faker
from redis import ConnectionPool
from django.conf import settings


faker = Faker(locale='zh_CN')

redis_conn_pool = ConnectionPool.from_url(
    settings.INFO_APP_REDIS, decode_responses=True)


def timestamp():
    return round(time.time()*1000)
