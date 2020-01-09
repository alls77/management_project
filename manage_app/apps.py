from django.apps import AppConfig


class ManageAppConfig(AppConfig):
    name = 'manage_app'

    def ready(self):
        import manage_app.signals
