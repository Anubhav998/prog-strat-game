from django.contrib import admin

from reversion import VersionAdmin
from matches.models import Match, Action


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = ['completed', 'arena']
    list_display = ['uuid', 'player_1', 'player_2', 'completed', 'timestamp', 'arena', 'victor', 'get_turn_count']


@admin.register(Action)
class ActionAdmin(VersionAdmin):
    pass