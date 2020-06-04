from . import validators
from ..models import *
from user.utils.serializers import UserInfoSerializer, UserField
from libs.rest.fields import PrimaryKeyRelatedField
from libs.rest.serializers import drf as serializers, ModelSerializer
from libs.rest.validators import (
    RelatedToOwnValidator, UniqueTogetherValidator, M2MNumValidator, RecursiveRelationValidator)


def pk_and_name(ins):
    return {'pk': ins.pk, 'name': ins.name}


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
    author = UserField()
    categories = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    tags = serializers.ManyRelatedField(
        PrimaryKeyRelatedField(pk_and_name, queryset=Tag.objects.all()), required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'category', 'categories', 'comment_count', 'excerpt', 'cover', 'content', 'like_count', 'liked')
        read_only_fields = ('created', 'updated',
                            'vote_count', 'comment_count', 'author', 'like_count')
        extra_kwargs = {
            'created': {'format': '%Y-%m-%d %H:%M:%S'},
            'updated': {'format': '%Y-%m-%d %H:%M:%S'},
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
        return []
        # res = []
        # n = 0
        # while cate is not None and n < 10:
        #     res.append({'id': cate.id, 'name': cate.name})
        #     cate = cate.parent
        #     n += 1
        # return res[::-1]

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
    author = UserField()
    child_count = serializers.SerializerMethodField()
    reply_to_author = serializers.SerializerMethodField()
    # children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'author', 'child_count',  'content', 'created', 'id', 'parent', 'post', 'reply_to', 'reply_to_author', 'like_count'
        )

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
