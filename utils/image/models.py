from django.db import models


class Hosting(models.Model):
    image = models.ForeignKey('ThirdPartyImage', on_delete=models.CASCADE, verbose_name='图片')
    url = models.URLField('图片链接', max_length=256)
    delete = models.URLField('删除图片链接', blank=True, null=True)

    class Meta:
        verbose_name = '图床链接'
        verbose_name_plural = verbose_name
        default_related_name = 'hostings'


class ThirdPartyImage(models.Model):
    description = models.CharField('描述', max_length=128, blank=True, null=True)
    created = models.DateField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        default_related_name = 'images'
