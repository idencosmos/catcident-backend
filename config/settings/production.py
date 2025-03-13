from .base import *

# -------------------------
# 로깅 설정
# -------------------------
LOGGING["handlers"]["console"] = {
    "class": "logging.StreamHandler",
    "formatter": "verbose",
    "level": "INFO",
}
LOGGING["loggers"]["uploads"]["handlers"] = ["console", "file"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 프로덕션 환경 추가 설정이 필요한 경우 여기에 작성합니다.
# 기본 설정은 대부분 .env 및 .env.prod 파일에서 로드됩니다.
