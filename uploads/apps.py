# uploads/apps.py
from django.apps import AppConfig


class UploadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploads'
    verbose_name = "File Uploads"

    def ready(self):
        import uploads.signals  # 시그널 연결