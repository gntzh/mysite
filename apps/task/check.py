import hashlib
import json
import random
import time

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class Check(object):
    app_info = {
        "appkey": "xisuncov",
        "url": "https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup",
    }
    url = {
        "login": "https://xxcapp.xidian.edu.cn/uc/wap/login/check",
        "login_status": "https://xxcapp.xidian.edu.cn/uc/wap/user/get-info",
        "check": "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save",
        "check_status": "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/index",
        "log": "https://xxcapp.xidian.edu.cn/wap/log/save-log",
        "origin": "https://xxcapp.xidian.edu.cn",
    }
    email_subject_tpl = "Check[{username}]：{event}{status}"
    email_content_tpl = "<p><strong>{detail}</strong><p/><p>{code}</p>"

    def __init__(self, email=None):
        self.email = email or "szhang_11@stu.xidian.edu.cn"

    def inform(self, email, subject, content):
        from_email = settings.DEFAULT_EMAIL_FROM
        mail = EmailMultiAlternatives(subject, content, from_email, [email,])
        mail.content_subtype = "html"
        mail_sent = mail.send()
        print(email, subject, content, sep="\n")

    def login(self, session, username, password):
        data = {
            "username": username,
            "password": password,
        }
        res = session.post(self.url["login"], data=data,)
        if res.status_code != requests.codes.ok:
            return False, "login失败"
        res = session.get(self.url["login_status"])
        if res.status_code == requests.codes.ok:
            try:
                if (data := res.json())["m"] == "操作成功" and data["d"]["base"]["role"][
                    "number"
                ] == username:
                    return True, data["d"]["base"]["email"]
                else:
                    return False, "login操作失败"
            except json.JSONDecodeError:
                return False, "login_status解析失败"
        else:
            return False, "login_status请求错误"

    def check(self, session):
        data = self.get_data()
        res = session.post(self.url["check"], data=data,)
        if res.status_code == requests.codes.ok:
            try:
                if res.json()["m"] == "操作成功":
                    return True, '...'
                else:
                    return False, "check操作失败"
            except json.JSONDecodeError:
                return False, "check解析错误"
        else:
            return False, "check请求错误"

    def check_status(self, session):
        res = session.get(self.url["check_status"])
        if res.status_code == requests.codes.ok:
            try:
                if (data := res.json())["m"] == "操作成功":
                    return data["d"]["realonly"], '...'
                else:
                    return None, "check_status操作失败"
            except json.JSONDecodeError:
                return None, "check_status解析错误"
        else:
            return False, "check_status请求错误"

    def log(self, session):
        data = {
            "timestamp": str(int(time.time())),
        }
        data.update(self.app_info)
        data["signature"] = hashlib.md5(
            bytes(data["appkey"] + data["timestamp"] + data["url"], "utf-8")
        ).hexdigest()
        res = session.post(self.url["log"], data=data)
        try:
            if res.status_code == requests.codes.ok and res.json()["m"] == "操作成功":
                return True, '...'
        except json.JSONDecodeError:
            return False, res.text

    def get_geo_data(self):
        data = random.choice(random.choice(list(self._geo_data.values())))
        if not isinstance(data["geo_api_info"], str):
            data["geo_api_info"] = json.dumps(data["geo_api_info"], ensure_ascii=False)
        return data

    def get_data(self):
        data = {
            "tw": random.randint(1, 2),
            "sfzx": 1,
            "sfcyglq": 0,
            "sfyzz": 0,
            "qtqk": "",
            "askforleave": 0,
        }
        data.update(self.get_geo_data())
        return data

    def make_session(self):
        session = requests.Session()
        session.headers.update(
            {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Origin": self.url["origin"],
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36 Edg/84.0.522.63",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        return session

    _geo_data = {
        "dorm": [
            {
                "area": "陕西省 西安市 长安区",
                "city": "西安市",
                "province": "陕西省",
                "address": "陕西省西安市长安区兴隆街道西安电子科技大学长安校区丁香公寓13号楼",
                "geo_api_info": {
                    "type": "complete",
                    "position": {
                        "Q": 34.122181260851,
                        "R": 108.82827446831601,
                        "lng": 108.828274,
                        "lat": 34.122181,
                    },
                    "location_type": "html5",
                    "message": "Get geolocation success.Convert Success.Get address success.",
                    "accuracy": 241,
                    "isConverted": True,
                    "status": 1,
                    "addressComponent": {
                        "citycode": "029",
                        "adcode": "610116",
                        "businessAreas": [],
                        "neighborhoodType": "",
                        "neighborhood": "",
                        "building": "",
                        "buildingType": "",
                        "street": "雷甘路",
                        "streetNumber": "266#",
                        "country": "中国",
                        "province": "陕西省",
                        "city": "西安市",
                        "district": "长安区",
                        "township": "兴隆街道",
                    },
                    "formattedAddress": "陕西省西安市长安区兴隆街道西安电子科技大学长安校区丁香公寓13号楼",
                    "roads": [],
                    "crosses": [],
                    "pois": [],
                    "info": "SUCCESS",
                },
            },
        ]
    }
