from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import RootComment, ChildComment


class RootCommentInline(GenericStackedInline):
    model = RootComment
    extra = 1


@admin.register(RootComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'created', ]
    list_filter = ['created', ]
    ordering = ('-created',)
    search_fields = ['content', ]


@admin.register(ChildComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'created', ]
    list_filter = ['created', ]
    ordering = ('-created',)
    search_fields = ['content', ]
