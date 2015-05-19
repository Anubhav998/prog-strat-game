from django.contrib import admin

from matches.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = ['completed', 'arena']
    list_display = ['uuid', 'player_1', 'player_2', 'completed', 'timestamp', 'arena', 'victor', 'get_turn_count']