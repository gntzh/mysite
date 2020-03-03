import json

from .backend import datetime, session, API
from apps.newpneumonia.models import Data


def parse_area_tree(node, path=None):
    if path is None:
        path = node.get('name')
    else:
        path = path + '/' + node.get('name')
    data = {}
    data['area'] = path
    data['date'] = datetime.now()
    data['new_confirm'] = node['today'].get('confirm')
    total = node['total']
    data['total_confirm'] = total.get('confirm')
    data['now_suspect'] = total.get('suspect')
    data['total_dead'] = total.get('dead')
    data['total_heal'] = total.get('heal')
    data['heal_rate'] = float(total.get('healRate'))
    data['dead_rate'] = total.get('deadRate')
    yield data
    children = node.get('children')
    if children is not None:
        for i in children:
            yield from parse_area_tree(i, path)


def run():
    res = session.get(API['global'])
    tree = json.loads(res.json()['data'])['areaTree']
    with open('global.json', 'w') as fp:
        json.dump(tree, fp)
    for node in tree:
        for i in parse_area_tree(node):
            print(i)
            Data.objects.update_or_create(
                i, date=i.get('date'), area=i['area'])
