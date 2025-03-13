from .base import *

# -------------------------
# 디버깅 도구 설정
# -------------------------
# Debug Toolbar
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]

# -------------------------
# 로깅 설정
# -------------------------
LOGGING["handlers"]["console"] = {
    "class": "logging.StreamHandler",
    "formatter": "verbose",
    "level": "DEBUG",
}
LOGGING["loggers"]["uploads"]["handlers"] = ["console", "file"]

# 개발 환경 추가 설정이 필요한 경우 여기에 작성합니다.
# 기본 설정은 대부분 .env 및 .env.dev 파일에서 로드됩니다.
