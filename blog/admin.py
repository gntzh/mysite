from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from comment.admin import RootCommentInline
from .models import *


class PostLikesInline(admin.TabularInline):
    model = PostLike
    extra = 1


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('pk', 'title', 'author', 'created', 'like_count')
    # list_select_related = False # 默认值, False时对外键字段使用select_related
    list_editable = ('title', )
    ordering = ('-updated', '-created', )

    search_fields = ('content', 'tags__name', 'category_name', )
    list_filter = ('created', 'updated', 'author', )

    fieldsets = [
        (None, {'fields': ('title', 'author')}),
        (None, {'fields': (('created', 'updated'),
                           ('is_public', 'allow_comments'),
                           ('comment_count'), 'category', 'tags', 'cover')}),
        ('内容', {'fields': ('content',)})
    ]
    filter_horizontal = ('tags',)

    inlines = [
        PostLikesInline,
        RootCommentInline,
    ]

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = '点赞'


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name', 'post_count', )
    list_display_links = ('indented_title', )

    mptt_level_indent = 20
    expand_tree_by_default = True

    search_fields = ('name', 'description',)

    fieldsets = [
        (None, {'fields': ('name', 'parent', 'description')}),
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_editable = ('name', )
    search_fields = ('name', )

    fieldsets = (
        (None, {'fields': ('name', )}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
