from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models import RootComment, ChildComment
from blog.models import Post
from user.utils.serializers import UserField

# TODO 修改其他的报错行为, 以字段映射字典返回更加详细的信息


class PostRootCommentSerializer(serializers.ModelSerializer):
    content_type = serializers.HiddenField(
        default=lambda: ContentType.objects.get_for_model(Post))
    post_id = serializers.IntegerField(source='object_id', label='文章id')
    owner = UserField()

    class Meta:
        model = RootComment
        fields = ('content_type', 'owner', 'id', 'post_id', 'vote_count', 'child_comment_count',
                  'created', 'content', )
        extra_kwargs = {
            'created': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
        }


def to_same_root_comment(data):
    if data['parent'] and data['root_comment'] and data['root_comment'] != data['parent'].root_comment:
        raise ValidationError({'root_comment': '子评论应与父评论对同一根评论进行评论'})


class PostChildCommentSerializer(serializers.ModelSerializer):
    content_type = serializers.HiddenField(
        default=ContentType.objects.get_for_model(Post))
    owner = UserField()

    class Meta:
        model = ChildComment
        fields = ('content_type', 'owner', 'id', 'root_comment', 'vote_count',
                  'created', 'content', )
        extra_kwargs = {
            'created': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
        }
        validators = [to_same_root_comment]


# def to_same_object(data):
#     if data['parent'] is not None and data['object_id'] != data['parent'].object_id:
#         raise ValidationError({'object_id': '子评论应与父评论对同一对象:父级评论'})

# class BlogCommentSerializer(serializers.ModelSerializer):
#     # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     content_type = serializers.HiddenField(
#         default=ContentType.objects.get_for_model(Post))
#     post_id = serializers.IntegerField(source='object_id', label='文章id')
#     owner_detail = serializers.SerializerMethodField()
#     parent_owner = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = ('content_type', 'owner', 'owner_detail', 'id', 'post_id',
#                   'parent', 'parent_owner', 'created', 'content', )
#         extra_kwargs = {
#             'created': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
#         }
#         validators = [to_same_object]

#     def get_owner_detail(self, obj):
#         return {'id': obj.owner.id, 'nickname': obj.owner.nickname, 'username': obj.owner.username, 'avatar': obj.owner.avatar}

#     def get_parent_owner(self, obj):
#         if obj.parent:
#             return {
#                 'id': obj.parent.id,
#                 'name': obj.parent.owner.nickname or obj.parent.owner.username,
#             }
#         return None
