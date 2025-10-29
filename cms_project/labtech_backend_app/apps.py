from django.apps import AppConfig

class LabtechBackendAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'labtech_backend_app'  # ✅ This should be 'labtech_backend_app' NOT 'lab'