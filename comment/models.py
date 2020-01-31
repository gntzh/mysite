from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.utils.functional import cached_property

allow_comments_models = Q()

for model in settings.ALLOW_COMMENTS_MODELS:
    allow_comments_models = allow_comments_models | Q(
        app_label=model[0], model=model[1])


class BaseComment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, verbose_name='创建者')
    created = models.DateTimeField('评论时间', auto_now_add=True)
    content = models.TextField('内容', max_length=512)
    vote_count = models.PositiveIntegerField('喜欢', default=0)

    class Meta:
        abstract = True


class RootComment(BaseComment):
    # 被评论的model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=allow_comments_models, verbose_name='ContentType')
    # 被评论的实例
    object_id = models.PositiveIntegerField('被评论的实例id')
    # 集中content_type和object_id, 便于ORM操作, 但该字段不存储任何数据
    content_object = GenericForeignKey('content_type', 'object_id')
    child_comment_count = models.PositiveIntegerField('二级评论数量', default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.content_object.comment_count = F('comment_count')+1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '根评论'
        verbose_name_plural = verbose_name
        default_related_name = 'root_comments'

    def __str__(self):
        return "<Comment(%s): %s>" % (self.id, self.content[:8])


class ChildComment(BaseComment):
    root_comment = models.ForeignKey(
        RootComment, models.CASCADE, related_query_name='child', related_name='children', verbose_name='根评论')
    reply_to = models.ForeignKey('self', models.DO_NOTHING,
                                 default=None,
                                 null=True,
                                 blank=True,
                                 related_query_name='reply',
                                 related_name='replies',
                                 verbose_name='父级评论')

    @cached_property
    def content_object(self):
        return self.root_comment.content_object

    def save(self, *args, **kwargs):
        if not self.pk:
            self.content_object.comment_count = F('comment_count') + 1
            self.content_object.save()
            self.root_comment.child_comment_count = F(
                'child_comment_count') + 1
            self.root_comment.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '二级评论'
        verbose_name_plural = verbose_name
        default_related_name = 'child_comments'

    def __str__(self):
        return "<Comment(%s): %s>" % (self.id, self.content[:8])


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, verbose_name='创建者')
    created = models.DateTimeField('评论时间', auto_now_add=True)
    content = models.TextField('内容', max_length=512)
    #  limit_choices_to=Q(parent__isnull=True) | Q(parent__parent__isnull=True)
    # 允许最多二级评论(保存时检查, 超过降级), 因此上面的限制也就没必要了
    parent = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.CASCADE,
                               related_query_name='child', related_name='children', verbose_name='父级评论',)

    # 被评论的model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=allow_comments_models, verbose_name='ContentType')
    # 被评论的实例
    object_id = models.PositiveIntegerField('被评论的实例id')
    # 集中content_type和object_id, 便于ORM操作, 但该字段不存储任何数据
    content_object = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        errors = {}
        # 检查与父级评论是否对同一对象评论
        if self.parent is not None:
            if self.content_type != self.parent.content_type or self.object_id != self.parent.object_id:
                errors = ValidationError(
                    '子评论应与父评论对同一对象:父级评论%s' % self.content_object).update_error_dict(errors)
        if errors:
            raise ValidationError(errors)

    def more_than_2(self):
        """检查是否超过二级
        """
        # if self.pk:
        #     return Comment.objects.filter(Q(pk=self.pk) & (Q(parent__isnull=True) | Q(parent__parent__isnull=True))).exists()
        # else:
        #     return bool(self.parent is None or self.parent.parent is None)
        return not (self.parent is None or self.parent.parent is None)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.content_type.get_all_objects_for_this_type(
                id=self.object_id).update(comment_count=F('comment_count')+1)
        if self.more_than_2():
            self.parent = self.parent.parent
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        default_related_name = 'comments'

    def __str__(self):
        return "<Comment(%s): %s>" % (self.id, self.content[:8])
