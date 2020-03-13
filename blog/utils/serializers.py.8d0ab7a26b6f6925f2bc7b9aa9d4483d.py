from . import validators
from ..models import Post, Tag, Category
from utils.rest.serializers import drf as serializers, ModelSerializer
from utils.rest.validators import (
    RelatedToOwnValidator, UniqueTogetherValidator, M2MNumValidator, RecursiveRelationValidator)


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
    category_display = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'author_id', 'author_display', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'tags_display', 'category', 'category_display', 'comment_count', 'excerpt', 'content', 'like_count', 'liked')
        read_only_fields = ('created', 'updated',
                            'vote_count', 'comment_count', 'author', 'like_count')
        extra_kwargs = {
            'created': {'format': '%Y-%m-%d %H:%M:%S'},
            'updated': {'format': '%Y-%m-%d %H:%M:%S'},
            'tags': {'write_only': True, 'validators': [RelatedToOwnValidator(True), M2MNumValidator(2), ]},
            'category': {'write_only': True, 'validators': [RelatedToOwnValidator(False), ]},
            'is_public': {'default': True},
        }

    def validate(self, data):
        if data.get('tags', False):
            RelatedToOwnValidator(True)(
                data['tags'], self.fields['tags'])
            M2MNumValidator(10)(data['tags'], self.fields['tags'])
        return data

    def get_category_display(self, row):
        if row.category is not None:
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

    def get_author_display(self, row):
        return {'id': row.author.id, 'username': row.author.username}

    def get_excerpt(self, obj):
        return obj.excerpt()

    def get_liked(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        return obj.likes.filter(pk=request.user.pk).exists()
