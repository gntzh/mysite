from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Hosting(models.Model):
    owner = models.ForeignKey(
        User, models.CASCADE, related_query_name='img_hosting', related_name='img_hostings', verbose_name='创建者')
    image = models.ForeignKey(
        'ThirdPartyImage', models.CASCADE, related_query_name='hosting', verbose_name='图片')
    url = models.URLField('图片链接', max_length=256)
    delete = models.URLField(
        '删除链接', max_length=256, blank=True, null=True, default=None)
    note = models.CharField('备注', max_length=256,
                            blank=True, null=True, default=None)

    class Meta:
        verbose_name = '图床链接'
        verbose_name_plural = verbose_name
        default_related_name = 'hostings'
        unique_together = ('url', 'owner', )


class ThirdPartyImage(models.Model):
    owner = models.ForeignKey(
        User, models.CASCADE, related_query_name='tp_image', related_name='tp_images', verbose_name='创建者')
    description = models.CharField(
        '描述', max_length=128, blank=True, null=True, default=None)
    created = models.DateField('创建时间', auto_now_add=True)
    album = models.ForeignKey('Album', models.CASCADE,
                              related_query_name='tp_image', blank=True, null=True, default=None)

    class Meta:
        verbose_name = '第三方图片'
        verbose_name_plural = verbose_name
        default_related_name = 'tp_images'

    def __str__(self):
        return "<TP_Image(%s):%s>" % (self.id, self.description[:8])


class Album(models.Model):
    name = models.CharField('名称', max_length=32)
    owner = models.ForeignKey(
        User, models.CASCADE, related_query_name='img_album', related_name='img_albums', verbose_name='创建者')
    created = models.DateField('创建时间', auto_now_add=True)
    description = models.CharField(
        '描述', max_length=128, blank=True, null=True, default=None)

    class Meta:
        verbose_name = '相册'
        verbose_name_plural = verbose_name
        unique_together = ['owner', 'name']
        default_related_name = 'albums'

    def __str__(self):
        return "<Album(%s):%s>" % (self.id, self.name[:8])
