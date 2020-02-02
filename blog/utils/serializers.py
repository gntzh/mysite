from . import validators
from ..models import Post, Tag, Category
from utils.rest.serializers import drf as serializers, ModelSerializer
from utils.rest.validators import (
    RelatedToOwnValidator, UniqueTogetherValidator, M2MNumValidator, RecursiveRelationValidator)


class TagSerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'owner', 'owner_id', 'post_count', 'posts']
        read_only_fields = ('owner_id', )
        extra_kwargs = {'owner': {'default': serializers.CurrentUserDefault()}}

    def get_post_count(self, row):
        return row.posts.count()

    def get_posts(self, row):
        return [{'id': post.id,
                 'title': post.title,
                 'created': post.created.strftime('%Y-%m-%d %H:%M:%S'), }
                for post in row.posts.all()]


class CategorySerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    is_leaf = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children',
                  'owner', 'owner_id', 'post_count', 'posts', 'is_leaf', 'siblings', )
        read_only_fields = ('owner_id', )
        extra_kwargs = {
            'parent': {'required': False, 'default': None, 'validators': (RelatedToOwnValidator(),)},
            'owner': {'default': serializers.CurrentUserDefault()},
        }
        validators = [UniqueTogetherValidator(
            Category.objects.all(), ['name', 'parent', 'owner']),
            UniqueTogetherValidator(
            Category.objects.filter(parent__isnull=True), ['name', 'parent', 'owner']),
            RecursiveRelationValidator()
        ]

    def get_siblings(self, row):
        if row.parent is None:
            siblings = Category.objects.filter(
                parent__isnull=True, owner=row.owner.id).only('name')
        else:
            siblings = Category.objects.filter(
                parent=row.parent.id, owner=row.owner.id).only('name')
        return [{'id': i.id,
                 'name': i.name, }
                for i in siblings]

    def get_children(self, row):
        return [{'id': i.id,
                 'name': i.name, }
                for i in row.children.all()]

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

    def get_is_leaf(self, row):
        return row.isLeaf()


class PostSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_display = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_id', 'author_display', 'is_public', 'allow_comments', 'created',
                  'updated', 'tags', 'tags_display', 'category', 'category_display', 'comment_count', 'excerpt', 'content', 'vote_count']
        read_only_fields = ('created', 'updated',
                            'vote_count', 'comment_count', 'author',)
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

    def get_excerpt(self, row):
        return row.excerpt()
