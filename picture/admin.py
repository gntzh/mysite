from django.contrib import admin
from .models import ThirdPartyImage, Hosting, Album


class TPImageInline(admin.StackedInline):
    model = ThirdPartyImage
    extra = 1


class HostingInline(admin.StackedInline):
    model = Hosting
    extra = 1


@admin.register(Hosting)
class HostingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'url', )

    fieldsets = [
        (None, {'fields': ('image', 'owner', 'url', 'delete', 'note', )}),
    ]


@admin.register(ThirdPartyImage)
class TPImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'owner', 'created', )

    fieldsets = [
        (None, {'fields': ('description', 'owner', 'album', )})
    ]

    inlines = (HostingInline, )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'owner', 'created', )
    # list_select_related = False # 默认值, False时对外键字段使用select_related
    list_editable = ('name', )
    ordering = ('-created', )

    search_fields = ('name', )
    list_filter = ('created', )

    fieldsets = [
        (None, {'fields': ('name', 'owner')}),
    ]

    inlines = (TPImageInline, )
