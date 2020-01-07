from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField('名称', max_length=32)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_query_name='tag', verbose_name='创建者')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        unique_together = ['owner', 'name']
        default_related_name = 'tags'

    def __str__(self):
        return "<Tag(%s):%s>" % (self.id, self.name[:8])


class Category(models.Model):
    name = models.CharField('名称', max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_query_name='category', verbose_name='创建者')
    parent = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.CASCADE,
                               related_query_name='child', related_name='children', verbose_name='父级分类')

    def validate_unique(self, exclude=None):
        try:
            if self.parent is None and Category.objects.exclude(id=self.id).filter(name=self.name, owner=self.owner,
                                                                                   parent__isnull=True).exists():
                raise ValidationError('字段 owner, name, parent 必须能构成唯一集合。')
        except AttributeError:
            pass
        super(Category, self).validate_unique(exclude)

    def clean(self):
        errors = {}
        if self.parent == self:
            errors['parent'] = '不允许将父级分类设为自己'
        parent_owner = getattr(self.parent, 'owner', None)
        if parent_owner is not None and parent_owner != self.owner:
            errors['parent'] = '不允许关联他人的分类'
        try:
            super(Category, self).clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        unique_together = ['owner', 'name', 'parent']
        default_related_name = 'categories'

    def postsNum(self):
        return self.posts.count()
    postsNum.short_description = '博客数量'

    def isRoot(self):
        if self.parent is None:
            return True
        return False

    def isLeaf(self):
        if self.children.exists():
            return False
        return True

    def getPosition(self):
        if self.isRoot():
            return 'root'
        elif self.isLeaf():
            return 'leaf'
        return 'sub'
    getPosition.short_description = '节点位置'

    def getLevel(self):
        level = 1
        node = self
        while not node.isRoot():
            level += 1
            node = node.parent
        return level

    def getLeafLevel(self):
        if self.isLeaf():
            return 0
        else:
            return 1 + max(node.getLeafLevel() for node in self.children.prefetch_related())

    def getLevels(self):
        return self.getLevel(), self.getLeafLevel()
    getLevels.short_description = '层数'

    def __str__(self):
        return "<Category(%s):%s>" % (self.id, self.name[:8])


class Post(models.Model):
    title = models.CharField('标题', max_length=64, default='无标题')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_query_name='post',
                               verbose_name='作者')
    is_public = models.BooleanField('是否公开', default=True)
    allow_comments = models.BooleanField('是否允许评论', default=True)
    created = models.DateTimeField('发布时间', auto_now_add=True)
    updated = models.DateTimeField('最近修改', auto_now=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name='分类',
                                 default=None,
                                 blank=True,
                                 null=True)
    tags = models.ManyToManyField(
        'Tag', blank=True, related_query_name='post', verbose_name='标签')
    content = models.TextField('内容', default='无内容')
    vote = models.PositiveIntegerField('点赞', default=0)

    comments = GenericRelation(Comment, related_query_name='post',)

    def clean(self):
        # 无法得到要保存的tags, 如果是修改self.tags.all()拿到的是旧数据
        # 如果是创建, 无法拿到连Manager都拿不到
        if self.category is not None and self.author != self.category.owner:
            raise ValidationError("不允许关联他人的分类<category(%s): %s>" % (
                self.category.id, self.category.name))
        super(Post, self).clean()

    def excerpt(self):
        return self.content[:64]

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name
        default_related_name = 'posts'

    def __str__(self):
        return "<Post(%s):%s>" % (self.id, self.title[:8])
