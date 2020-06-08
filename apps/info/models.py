from django.db import models


# XXX 频次高时考虑放到redis, 或者加缓存
# TODO 关键词和微博类型使用django3.1的JSON字段
class WeiBoUser(models.Model):
    uid = models.CharField('UID', max_length=64, unique=True)
    username = models.CharField('用户名', max_length=128, )
    # keywords = models.TextField('关键词', default='')
    # feature = models.CharField('微博类型')
