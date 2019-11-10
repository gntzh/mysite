from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    nickname = models.CharField(max_length=32, default="", verbose_name="昵称")
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', "email_is_active")}),
        (_('Personal info'), {'fields': ('nickname', )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ["username", "email", "email_is_active", "is_superuser", "is_staff", "is_active"]
