from django.apps import AppConfig


class MatchesConfig(AppConfig):
    name = 'matches'
    verbose_name = 'Matches'

    def ready(self):
        from matches import signals