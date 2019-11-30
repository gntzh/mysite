from django.contrib import admin
from .models import Post, Tag, Category
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', "created"]
    list_filter = ['created', 'updated']
    ordering = ('-updated', '-created', )
    search_fields = ['content', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    ordering = ('name', )
    search_fields = ['name', ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ('name', )
    search_fields = ['name', ]