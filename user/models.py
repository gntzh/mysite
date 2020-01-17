from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=32, blank=True)
    avatar = models.URLField(blank=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True,)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email_is_active = models.BooleanField(verbose_name='邮箱状态', default=False)
    created = models.DateTimeField("注册时间", auto_now_add=True)
    sign = models.CharField(max_length=128, verbose_name='个人签名', blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
