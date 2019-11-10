from datetime import datetime
import pyDes
import base64
import binascii
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

User = get_user_model()


def getDesMethod(user):
    key = bytes(str(user.created_time)[-16:-8], encoding="utf-8")
    iv = key
    method = pyDes.des(key, mode=pyDes.CBC, IV=iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return method


def generateVerifyEmailUrl(user):
    if isinstance(user, User):
        try:
            data = bytes(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "@" + str(user.id) + "@" + user.username, encoding="utf-8")
            method = getDesMethod(user)
            token = binascii.b2a_hex(method.encrypt(data, padmode=pyDes.PAD_PKCS5))
            user_id = bytes(str(user.id), encoding="utf-8")
            key = base64.b64encode(b"%s@%s" % (token, user_id,)).decode("utf-8")
            verify_url = '%s/api-user/verify_email?key=%s' % (settings.SITE_HOST, key)
            return verify_url
        except:
            return False


def checkVerifyEmailUrl(key):
    token, user_id = base64.b64decode(key.encode("utf-8")).decode("utf-8").split("@")
    user_id = int(user_id)
    user = User.objects.get(id=user_id)
    method = getDesMethod(user)
    data = method.decrypt(binascii.a2b_hex(token.encode("utf-8")), padmode=pyDes.PAD_PKCS5).decode("utf-8")
    print(data)
    now = datetime.now()
    created_time, id_data, username = data.split("@")
    created_time = datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
    delta = int((now - created_time).seconds)
    if delta > 60*60*6:
        return False, user
    else:
        return True, user


def sendVerifyEmail(user, verify_url):
    subject = "Shoor's Site 用户%s邮箱验证" % user.username
    to_email = user.email
    from_email = settings.DEFAULT_EMAIL_FROM
    text_content = "欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s" % verify_url
    html_content = "<p>欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s </p>" % verify_url
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to_email, ])
    mail.attach_alternative(html_content, "text/html")
    mail.send()
