from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework_simplejwt.tokens import Token, TokenError


User = get_user_model()


class EmailVerifyToken(Token):
    token_type = 'email_verify'
    lifetime = timedelta(minutes=15)


def generateVerifyEmailUrl(user):
    verify_url = '%s/api-user/verify_email?key=%s' % (
        settings.SITE_HOST, EmailVerifyToken.for_user(user))
    return verify_url


def checkVerifyEmailUrl(key):
    try:
        token = EmailVerifyToken(key)
    except TokenError:
        return False, None
    else:
        return True, User.objects.get(id=token['user_id'])


def sendVerifyEmail(user, verify_url):
    subject = "Shoor's Site 用户%s邮箱验证" % user.username
    to_email = user.email
    from_email = settings.DEFAULT_EMAIL_FROM
    text_content = "欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s" % verify_url
    html_content = "<p>欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s </p>" % verify_url
    mail = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email, ])
    mail.attach_alternative(html_content, 'text/html')
    mail.send()
