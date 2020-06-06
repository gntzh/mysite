import re
from lxml.etree import HTML
import requests
from apps.info.utils import timestamp, faker

a_pattern = re.compile(r'<a.*?href="(.+?)".*?>(.*)</a>')


def baidu_calendar(month, day):
    month = f'{month:0>2d}'
    day = f'{day:0>2d}'
    params = {'_': timestamp()}
    headers = {
        'User-Agent': faker.chrome(version_from=53),
        'Referer': 'https://baike.baidu.com/calendar/'
    }
    res = requests.get(
        f'https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json', headers=headers)
    data = res.json()[month][month + day]
    events = []
    for i in data:
        e = {}
        match = a_pattern.search(i['title'])
        e['messageURL'] = 'https://baike.baidu.com/calendar/' if match is None else match.group(
            1)
        e['title'] = f'{i["year"]}年的今天，' + \
            a_pattern.sub('\g<2>', i['title'].strip())
        if i['cover']:
            e['picURL'] = i['pic_share']
            events.insert(0, e)
        else:
            events.append(e)
    return events


def lssdjt(month, day):
    params = {'date': f'{month}-{day}'}
    headers = {
        'User-Agent': faker.chrome(version_from=53),
    }
    res = requests.get('http://m.lssdjt.com/', params, headers=headers)
    res.encoding = 'UTF-8'
    hot_list = HTML(res.text).xpath('//div[@class="list"]/li/a')[::-1]
    res = requests.get('http://www.lssdjt.com/', params, headers=headers)
    res.encoding = 'UTF-8'
    img_list = HTML(res.text).xpath('//ul[contains(@class,"list")]/li/a')
    events = []
    for hot, img in zip(hot_list, img_list):
        if hot.xpath('img'):
            e = {}
            e['title'] = hot.text
            if e['title'].startswith('-'):
                e['title'].replace('-', '公元前', 1)
            e['messageURL'] = 'http://m.lssdjt.com'+hot.xpath('@href')[0]
            rel = img.xpath('@rel')
            if rel:
                e['picURL'] = rel[0]
            events.append(e)
    return events
