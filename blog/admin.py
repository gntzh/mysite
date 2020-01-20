from django.contrib import admin
from .models import Post, Tag, Category
from comment.admin import CommentInline


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('pk', 'title', 'author', 'created')
    # list_select_related = False # 默认值, False时对外键字段使用select_related
    list_editable = ('title', )
    ordering = ('-updated', '-created', )

    search_fields = ('content', 'tags__name', 'category_name', )
    list_filter = ('created', 'updated', 'author', )

    fieldsets = [
        (None, {'fields': ('title', 'author')}),
        (None, {'fields': (('is_public', 'allow_comments'), 'vote', 'category', 'tags')}),
        ('内容', {'fields': ('content',)})
    ]
    filter_horizontal = ('tags',)

    inlines = [
        CommentInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'owner', 'post_count', 'getPosition',)
    list_editable = ('name', )  # 若添加'parent'字段 SQL查询重复太多
    # empty_value_display = '无父级分类'
    ordering = ('name', )

    search_fields = ('name', )
    list_filter = ('parent', 'owner', )

    fieldsets = [
        (None, {'fields': ('name', 'owner', 'parent', )}),
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', )
    list_editable = ('name', )
    search_fields = ('name', )

    list_filter = ('owner', )

    fieldsets = [
        (None, {'fields': ('name', 'owner', )}),
    ]
