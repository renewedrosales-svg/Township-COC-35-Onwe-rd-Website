from django.apps import AppConfig


class ChurchSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.church_settings'

    def ready(self):
        import apps.church_settings.signals  # noqa: F401