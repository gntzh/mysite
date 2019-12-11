from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db.models import Q

allow_comments_models = Q()

for model in settings.ALLOW_COMMENTS_MODELS:
    allow_comments_models = allow_comments_models | Q(
        app_label=model[0], model=model[1])


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, verbose_name='创建者')
    created = models.DateTimeField('评论时间', auto_now_add=True)
    content = models.TextField('内容', max_length=512)
    parent = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.CASCADE,
                               related_query_name='child', related_name='children', verbose_name='父级评论')

    # 被评论的model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=allow_comments_models, verbose_name='ContentType')
    # 被评论的实例
    object_id = models.PositiveIntegerField('被评论的实例id')
    # 集中content_type和object_id, 便于ORM操作, 但该字段不存储任何数据
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        default_related_name = 'comments'

    def __str__(self):
        return "<%s: %s>" % (self.owner.username, self.content[:8])
