from django.contrib import admin
from .models import Data


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'area',
        'date',
        'updated_at',
        'now_suspect',
        'now_confirm',
        'now_severe',
        'new_confirm',
        'new_suspect',
        'new_heal',
        'new_dead',
        'total_confirm',
        'total_heal',
        'total_dead',
        'heal_rate',
        'dead_rate',
    )
    list_filter = ('date', 'updated_at')
    date_hierarchy = 'updated_at'
