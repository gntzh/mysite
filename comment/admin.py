from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Comment


class CommentInline(GenericStackedInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'parent', 'created', ]
    list_filter = ['created', ]
    ordering = ('-created',)
    search_fields = ['content', ]
