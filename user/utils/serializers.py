from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from . import validators

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "email_is_active",
                  "nickname", "last_login", "logo", "phone"]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"write_only": True, "required": True, "help_text": "必填"},
            "email": {"label": "邮箱"},
            "email_is_active": {"read_only": True},
            "last_login": {"read_only": True, 'format': '%Y-%m-%d %H:%M:%S'},
            "groups": {"default": Group.objects.get(pk=1), "read_only": True,},
            "logo": {"help_text": "一个URL"}
        }
        validators = [validators.CheckUsername]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "nickname", "logo", "phone", "old_password"]
        extra_kwargs = {
            "password": {"required": False},
            "email": {"label": "邮箱", "required": False},
            "groups": {"default": Group.objects.get(pk=1), },
            "username": {"required": True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            user = super().update(instance, validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user
        return super().update(instance, validated_data)

