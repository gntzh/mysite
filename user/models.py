from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=32, blank=True)
    avatar = models.URLField(blank=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", blank=True)
    email = models.EmailField(
        _('email address'), null=True, blank=True, unique=True,)
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
    comment_count = models.PositiveIntegerField('留言数', default=0, )

    def save(self, *args, **kwargs):
        # 对于进行唯一性约束的string field(空值默认约定为空字符串),强制修改为null
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class OUser(models.Model):
    identity_types = (
        ('gh', 'Github'),
        ('wb', '微博'),
    )
    user = models.ForeignKey(User, models.CASCADE,
                             related_query_name='ouser', verbose_name='站内用户')
    identifier = models.CharField(max_length=256, verbose_name='唯一且不变标识')
    identity_type = models.CharField(
        max_length=2, choices=identity_types, verbose_name='平台')
    # credential

    class Meta:
        verbose_name = '其他用户'
        verbose_name_plural = verbose_name
        default_related_name = 'ousers'
        unique_together = ('identity_type', 'identifier')
