from datetime import datetime, timedelta, timezone
import json
from faker import Faker
import requests


beijing = timezone(timedelta(hours=8), "Beijing")


def strptime(s: str):
    m, d = [int(i) for i in s.split(".")]
    return datetime(2020, m, d).replace(tzinfo=beijing)


API = {
    'global': 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5',
    'others': 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other',
}

faker = Faker('zh_CN')
session = requests.Session()
session.headers.update({'user_agent': faker.user_agent()})
