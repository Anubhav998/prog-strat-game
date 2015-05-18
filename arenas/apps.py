from django.apps import AppConfig


class ArenasConfig(AppConfig):
    name = 'arenas'
    verbose_name = 'Arenas'

    def ready(self):
        from arenas import signals