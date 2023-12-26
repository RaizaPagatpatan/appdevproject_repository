from django.apps import AppConfig


class EveappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eveapp'
    def ready(self):
        import eveapp.signals
