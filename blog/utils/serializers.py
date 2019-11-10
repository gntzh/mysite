from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .. import models


class TagSerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_num = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_post_num(self, row):
        return row.posts.count()

    def get_posts(self, row):
        return [(post.id, post.title) for post in row.posts.all()]

    class Meta:
        model = models.Tag
        fields = ["id", "name", "owner", "post_num", "posts"]
        extra_kwargs = {
            "post_num": {"read_only": True},
        }


class CategorySerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_num = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_post_num(self, row):
        return row.posts.count()

    def get_posts(self, row):
        return [(post.id, post.title) for post in row.posts.all()]

    class Meta:
        model = models.Category
        fields = ["id", "name", "owner", "post_num", "posts"]
        extra_kwargs = {
            "post_num": {"read_only": True},
        }


class PostSerializer(ModelSerializer):
    author_display = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_category_display(self, row):
        return {"id": row.category.id, "name": row.category.name}

    def get_tags_display(self, row):
        return ({"id":tag.id, "name": tag.name} for tag in row.tags.all())

    def get_author_display(self, row):
        return {"id": row.author.id, "username": row.author.username}

    class Meta:
        model = models.Post
        fields = ["id", "title", "author", "author_display", "is_public", "allow_comments", "created_time",
                  "modified_time", "tags", 'tags_display', "category", "category_display", "content", "vote"]
        extra_kwargs = {
            # "title": {"required": False,},
            # "content": {"requiresd": False, },
            "created_time": {"read_only": True, 'format': '%Y-%m-%d %H:%M:%S'},
            "modified_time": {"read_only": True, 'format': '%Y-%m-%d %H:%M:%S'},
            "tags": {"write_only": True},
            "category": {"write_only": True},
            "tags_display": {"read_only": True},
            "category_display": {"read_only": True},
            "author_display": {"read_only": True},
            "vote": {"read_only": True},
        }
