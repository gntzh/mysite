from utils.rest.serializers import drf as serializers, ModelSerializer

from .. import models
from . import validators


class TagSerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_num = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'owner', 'post_num', 'posts']
        extra_kwargs = {}

    def get_post_num(self, row):
        return row.posts.count()

    def get_posts(self, row):
        return [{'id': post.id,
                 'title': post.title,
                 'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
                 'author': post.author.username}
                for post in row.posts.all()]


class CategorySerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_num = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    is_leaf = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent', 'children',
                  'owner', 'post_num', 'posts', 'is_leaf']
        extra_kwargs = {
            'parent': {'required': False, 'default': None}
        }
        validators = [validators.UniqueTogetherValidator(
            models.Category.objects.all(), ['name', 'parent', 'owner'])]

    def validate(self, data):
        data = validators.uniqueCate(data)
        data = validators.validateParent(data)
        return data

    def get_children(self, row):
        return [{'id': i.id,
                 'name': i.name, }
                for i in row.children.all()]

    def get_post_num(self, row):
        return row.postsNum()

    def get_posts(self, row):
        return [{'id': post.id,
                 'title': post.title,
                 'created': post.created.strftime('%Y-%m-%d %H:%M:%S'),
                 'author': post.author.username}
                for post in row.posts.all()]

    def get_is_leaf(self, row):
        return row.isLeaf()



class PostSerializer(ModelSerializer):
    author_display = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = ['id', 'title', 'author', 'author_display', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'tags_display', 'category', 'category_display', 'excerpt', 'content', 'vote']
        extra_kwargs = {
            # 'title': {'required': False,},
            # 'content': {'requiresd': False, },
            'created': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
            'updated': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
            'tags': {'write_only': True},
            'category': {'write_only': True},
            'vote': {'read_only': True},
            'is_public': {'default': True},
            'tags_display': {'read_only': True},
            'category_display': {'read_only': True},
            'author_display': {'read_only': True},
        }

    def validate(self, data):
        data = validators.ownerTag(data)
        return data

    def get_category_display(self, row):
        if row.category is not None:
            return {'id': row.category.id, 'name': row.category.name}
        return {}

    def get_tags_display(self, row):
        return ({'id': tag.id, 'name': tag.name} for tag in row.tags.all())

    def get_author_display(self, row):
        return {'id': row.author.id, 'username': row.author.username}

    def get_excerpt(self, row):
        return row.excerpt()
