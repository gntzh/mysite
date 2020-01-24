from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from blog.models import Post
from ..models import Comment

# TODO 修改其他的报错行为, 以字段映射字典返回更加详细的信息
def to_same_object(data):
    if data['parent'] is not None and data['object_id'] != data['parent'].object_id:
        raise ValidationError({'object_id': '子评论应与父评论对同一对象:父级评论'})


class BlogCommentSerializer(serializers.ModelSerializer):
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content_type = serializers.HiddenField(
        default=ContentType.objects.get_for_model(Post))
    post_id = serializers.IntegerField(source='object_id', label='文章id')

    class Meta:
        model = Comment
        fields = ('content_type', 'owner', 'id', 'post_id',
                  'parent', 'created', 'content', )
        extra_kwargs = {
            'created': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
        }
        validators = [to_same_object]
