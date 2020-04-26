from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

from comment.models import BaseComment

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField('名称', max_length=32)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_query_name='tag', verbose_name='创建者')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        default_related_name = 'tags'

    def __str__(self):
        return "<Tag(%s):%s>" % (self.id, self.name[:8])


class Category(MPTTModel):
    name = models.CharField('名称', max_length=64, unique=True)
    description = models.CharField('描述', max_length=1024, default='暂无描述')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        default_related_name = 'categories'

    def post_count(self):
        return self.posts.count()
    post_count.short_description = '博客数量'

    def __str__(self):
        return "<Category(%s):%s>" % (self.id, self.name[:8])


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(is_public=True)


class Post(models.Model):
    title = models.CharField('标题', max_length=64, default='无标题')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_query_name='post',
                               verbose_name='作者')
    is_public = models.BooleanField('是否公开', default=True)
    allow_comments = models.BooleanField('是否允许评论', default=True)
    created = models.DateTimeField('发布时间', default=timezone.now)
    updated = models.DateTimeField('最近修改', default=timezone.now)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name='分类',
                                 related_query_name='post',
                                 default=None,
                                 blank=True,
                                 null=True)
    tags = models.ManyToManyField(
        'Tag', blank=True, related_query_name='post', verbose_name='标签')
    cover = models.URLField('题图', max_length=256,
                            blank=True, null=True, default=None)
    content = models.TextField('内容', default='无内容')

    likes = models.ManyToManyField(
        User, through='PostLike', related_name='liked_posts', verbose_name='点赞')
    like_count = models.PositiveIntegerField('点赞量', default=0)

    need_index = models.BooleanField('更新搜索索引', default=True)

    comment_count = models.PositiveIntegerField('评论数', default=0)

    objects = models.Manager()
    public = PublicManager()

    def excerpt(self):
        return self.content[:64]

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name
        default_related_name = 'posts'

    def __str__(self):
        return '%s' % self.title[:16]


class PostLike(models.Model):
    user = models.ForeignKey(User, models.CASCADE, )
    post = models.ForeignKey(Post, models.CASCADE, )

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'post')
        default_related_name = 'post_likes'

    def __str__(self):
        return '{} 点赞了 {}'.format(self.user, self.post)


class Comment(BaseComment):
    object_field = 'post'
    post = models.ForeignKey(Post, models.CASCADE)


__all__ = ['Category', 'Comment', 'Post', 'PostLike', 'Tag', ]
