from django.db import models


class Data(models.Model):
    area = models.CharField('地区', max_length=32)
    date = models.DateField('日期')
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    now_suspect = models.IntegerField('现存疑似', null=True, default=None)
    now_confirm = models.IntegerField('现存确诊', null=True, default=None)
    now_severe = models.IntegerField('现存确诊', null=True, default=None)

    confirm_cuts = models.IntegerField('现存确诊', null=True, default=None)

    new_confirm = models.IntegerField('新增确诊',  null=True, default=None)
    new_suspect = models.IntegerField('新增疑似', null=True, default=None)
    new_heal = models.IntegerField('新增治愈', null=True, default=None)
    new_dead = models.IntegerField('新增死亡', null=True, default=None)

    total_confirm = models.IntegerField('累计确诊',  null=True, default=None)
    total_heal = models.IntegerField('累计治愈',  null=True, default=None)
    total_dead = models.IntegerField('累计死亡', null=True, default=None)

    heal_rate = models.FloatField('治愈率',  null=True, default=None)
    dead_rate = models.FloatField('死亡率', null=True, default=None)

    class Meta:
        verbose_name = '肺炎数据'
        verbose_name_plural = verbose_name
        unique_together = ['area', 'date']
