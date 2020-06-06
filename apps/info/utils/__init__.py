import time
from faker import Faker

faker = Faker(locale='zh_CN')


def timestamp():
    return round(time.time()*1000)
