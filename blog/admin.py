from django.contrib import admin
from .models import Post, Tag, Category
from comment.admin import CommentInline


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'created']
    list_filter = ['created', 'updated']
    ordering = ('-updated', '-created', )
    search_fields = ['content', ]

    inlines = [
        CommentInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'owner']
    ordering = ('name', )
    search_fields = ['name', ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']
    ordering = ('name', )
    search_fields = ['name', ]
