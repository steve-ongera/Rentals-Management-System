from django.apps import AppConfig


class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Rentals'

    def ready(self):
        import Rentals.signals  # Import the signals module to register signals
