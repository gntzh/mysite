from . import validators
from ..models import *
from user.utils.serializers import UserInfoSerializer
from utils.rest.serializers import drf as serializers, ModelSerializer
from utils.rest.validators import (
    RelatedToOwnValidator, UniqueTogetherValidator, M2MNumValidator, RecursiveRelationValidator)

# TODO 取消author_display字段, 改为author和author_配合


class TagSerializer(ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    post_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'post_count', 'posts', 'created_by']
        read_only_fields = ()
        extra_kwargs = {}

    def get_post_count(self, row):
        return row.posts.count()

    def get_posts(self, row):
        return [{'id': post.id,
                 'title': post.title,
                 'created': post.created.strftime('%Y-%m-%d %H:%M:%S'), }
                for post in row.posts.all()]


class CategorySerializer(ModelSerializer):
    post_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'post_count', 'posts', 'description')
        read_only_fields = ()
        extra_kwargs = {}
        validators = []

    def get_post_count(self, row):
        # return getattr(row, 'post_count', row.posts.count())
        return row.posts.count()

    def get_posts(self, row):
        # assert self.instance is row
        return [{'id': post.id,
                 'title': post.title,
                 'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
                 }
                for post in row.posts.all()]


class PostSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_display = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'author_id', 'author_display', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'tags_display', 'category', 'categories', 'comment_count', 'excerpt', 'cover', 'content', 'like_count', 'liked')
        read_only_fields = ('created', 'updated',
                            'vote_count', 'comment_count', 'author', 'like_count')
        extra_kwargs = {
            'created': {'format': '%Y-%m-%d %H:%M:%S'},
            'updated': {'format': '%Y-%m-%d %H:%M:%S'},
            'tags': {'write_only': True, },
            'category': {'write_only': True, },
            'is_public': {'default': True},
        }

    def validate(self, data):
        if data.get('tags', False):
            M2MNumValidator(10)(data['tags'], self.fields['tags'])
        return data

    def get_categories(self, row):
        if row.category is not None:
            return [{'id': c.id, 'name': c.name} for c in row.category.get_ancestors(include_self=True)]
            return {"id": row.category.id, "name": row.category.name}
        return None
        # res = []
        # n = 0
        # while cate is not None and n < 10:
        #     res.append({'id': cate.id, 'name': cate.name})
        #     cate = cate.parent
        #     n += 1
        # return res[::-1]

    def get_tags_display(self, row):
        return ({'id': tag.id, 'name': tag.name} for tag in row.tags.all())

    def get_author_display(self, instance):
        return UserInfoSerializer(instance.author).data

    def get_excerpt(self, obj):
        return obj.excerpt()

    def get_liked(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        return obj.likes.filter(pk=request.user.pk).exists()


class CommentSerializer(ModelSerializer):
    author_ = serializers.HiddenField(
        source='author', default=serializers.CurrentUserDefault())
    author = serializers.SerializerMethodField()
    child_count = serializers.SerializerMethodField()
    reply_to_author = serializers.SerializerMethodField()
    # children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'author', 'author_', 'child_count',  'content', 'created', 'id', 'parent', 'post', 'reply_to', 'reply_to_author', 'like_count'
        )

    def get_author(self, instance):
        return UserInfoSerializer(instance.author).data

    def get_child_count(self, instance):
        return instance.children.count()

    def get_children(self, instance):
        return [{
            'id': child.id,
            'content': child.content,
            'created': child.created,
            'author': UserInfoSerializer(child.author).data
        } for child in instance.children.all()[:5]]

    def get_reply_to_author(self, instance):
        if instance.parent is not None:
            return UserInfoSerializer(instance.parent.author).data
        return None


class LocalPostSerializer(PostSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'category', 'cover', 'content', )
