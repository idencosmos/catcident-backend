# uploads/apps.py
# 미디어 파일 관리 앱 설정
# 앱 초기화 시 시그널 처리를 위한 진입점
from django.apps import AppConfig


class UploadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "uploads"
    verbose_name = "SysMedia Uploads"

    def ready(self):
        # 시그널 모듈을 임포트하여 시그널 핸들러를 등록
        import uploads.signals
