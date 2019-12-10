from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField('名称', max_length=32)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="创建者")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        unique_together = ["owner", "name"]
        default_related_name = 'tags'

    def __str__(self):
        return self.name[:8]


# 暂留一坑, 多级分类
class Category(models.Model):
    name = models.CharField('名称', max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name="父级分类", related_name="subs")

    def validate_unique(self, exclude=None):
        if self.parent is None and Category.objects.exclude(id=self.id).filter(name=self.name, owner=self.owner, parent__isnull=True).exists():
            raise ValidationError("字段 owner, name, parent 必须能构成唯一集合。")
        super(Category, self).validate_unique(exclude)

    def clean(self):
        if self.parent == self:
            raise ValidationError("不允许将父级分类设为自己")
        parent_owner = getattr(self.parent, 'owner', None)
        print(parent_owner)
        if parent_owner is not None and parent_owner != self.owner:
            raise ValidationError("不允许关联他人的分类")
        super(Category, self).clean()

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        unique_together = ["owner", "name", "parent"]
        default_related_name = 'categories'

    def __str__(self):
        return self.name[:16]


class Post(models.Model):
    title = models.CharField('标题', max_length=64, default="无标题")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='作者')
    is_public = models.BooleanField("是否公开", default=True)
    allow_comments = models.BooleanField("是否允许评论", default=True)
    created = models.DateTimeField('发布时间', auto_now_add=True)
    updated = models.DateTimeField('最近修改', auto_now=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='分类',
                                 blank=True,
                                 null=True)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    content = models.TextField('内容', default="无内容")
    vote = models.PositiveIntegerField("点赞", default=0)

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name
        default_related_name = 'posts'

    def __str__(self):
        return self.title[:32]

    def excerpt(self):
        return self.content[:64]
