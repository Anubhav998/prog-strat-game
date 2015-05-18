from django.contrib import admin

from arenas.models import Arena


@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_size_display']