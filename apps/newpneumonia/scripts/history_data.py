import json
from apps.newpneumonia.models import Data
from .backend import strptime, datetime, session, API


def get_data(url):
    res = session.get(url)
    return json.loads(res.json()['data'])


def parse_other_data(data):
    history = {}
    for i in data['chinaDayList']:
        history['area'] = '中国'
        history['date'] = strptime(i.get('date'))
        history['total_confirm'] = i.get('confirm')
        history['total_heal'] = i.get('heal')
        history['total_dead'] = i.get('dead')
        history['now_suspect'] = i.get('suspect')
        history['now_confirm'] = i.get('nowConfirm')
        history['now_severe'] = i.get('nowSevere',)
        history['heal_rate'] = i.get('healRate')
        history['dead_rate'] = i.get('deadRate')
        yield history

    # for i in data['chinaDayList']:
    #     history['date'] = strptime(i.get('date'))
    #     history['confirm'] = i.get('confirm')
    #     history['suspect'] = i.get('suspect')
    #     history['heal'] = i.get('heal')
    #     history['dead'] = i.get('dead')
    #     yield history


def run():
    data = get_data(API['others'])
    with open('others.json', 'w') as fp:
        json.dump(data, fp)
    for i in parse_other_data(data):
        print(i)
        Data.objects.update_or_create(i, date=i.get('date'), area=i['area'])
