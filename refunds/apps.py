from django.apps import AppConfig

class RefundsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'refunds'

    def ready(self):
        import refunds.signals  # Connecting signals to handle status updates via email
