# config/settings/base.py
"""
기본 Django 설정 파일
개발 및 프로덕션 환경에서 공통으로 사용되는 설정들이 포함됩니다.
"""

import environ
import os
from pathlib import Path

# =================================================
# 기본 설정 및 환경변수
# =================================================
# 환경변수 초기화
env = environ.Env(DEBUG=(bool, False))

# 프로젝트 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 기본 .env 파일 로드 (공통 설정)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# 환경별 .env 파일 로드 (개발 또는 프로덕션)
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")
if DJANGO_ENV == "production":
    environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))
else:
    environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

# 로그 디렉토리 생성
LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 코어 설정
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# =================================================
# Next.js 재검증 설정
# =================================================
# Next.js 재검증 API URL
NEXTJS_REVALIDATE_URL = env("NEXTJS_REVALIDATE_URL", default=None)
# Next.js 재검증 API 토큰 (보안을 위해)
NEXTJS_REVALIDATE_TOKEN = env("NEXTJS_REVALIDATE_TOKEN", default=None)

# =================================================
# 애플리케이션 정의
# =================================================
INSTALLED_APPS = [
    # Django 기본 앱
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 보안 관련 앱
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_email",
    # 서드파티 앱
    "rest_framework",
    "corsheaders",
    "django_ckeditor_5",
    "parler",
    "storages",
    "django_celery_beat",
    # 헬스체크 앱
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    # 프로젝트 앱
    "accounts",
    "homepage",
    "uploads",
]

# =================================================
# 미들웨어 설정
# =================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",  # AuthenticationMiddleware 다음에 위치
    "accounts.middleware.OTPSetupMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =================================================
# URL 및 템플릿 설정
# =================================================
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =================================================
# 데이터베이스 설정
# =================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT", default=5432),
    }
}

# =================================================
# 보안 설정
# =================================================
# CORS 설정
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# 비밀번호 유효성 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 인증 및 세션 설정
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 86400  # 24시간
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)

# SSL 보안 설정
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SECURE_CONTENT_TYPE_NOSNIFF", default=False)
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=False)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# 사용자 모델
AUTH_USER_MODEL = "accounts.CustomUser"

# OTP 인증 설정
OTP_TOTP_ISSUER = "Catcident API"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
OTP_EMAIL_SUBJECT = "Your OTP Token"
OTP_EMAIL_BODY_TEMPLATE = "Your one-time password is: {{ token }}"

# =================================================
# 국제화 설정
# =================================================
LANGUAGE_CODE = "ko"  # 기본 언어
LANGUAGES = (
    ("ko", "Korean"),
    ("en", "English"),
)

PARLER_LANGUAGES = {
    None: (  # 기본 사이트
        {"code": "ko"},
        {"code": "en"},
    ),
    "default": {
        "fallbacks": ["ko"],  # ko를 fallback 언어로
        "hide_untranslated": False,
    },
}

TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# =================================================
# 파일 저장소 설정
# =================================================
# R2 설정
R2_BUCKET_NAME = env("R2_BUCKET_NAME")
R2_REGION = env("R2_REGION", default="auto")
R2_ENDPOINT_URL = env("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY")

# 정적 파일 설정
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = "staticfiles"

# 미디어 파일 설정
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = "media"
MEDIA_PUBLIC_DOMAIN = env("MEDIA_PUBLIC_DOMAIN")

# 스토리지 백엔드
STORAGES = {
    "staticfiles": {"BACKEND": env("STATICFILES_STORAGE")},
    "default": {"BACKEND": env("DEFAULT_FILE_STORAGE")},
}

# =================================================
# API 및 DB 설정
# =================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF 설정
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# =================================================
# Celery 및 캐싱 설정
# =================================================
# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True  # 이 줄 추가

# 주기적 작업
CELERY_BEAT_SCHEDULE = {
    "clean-unused-media-every-day": {
        "task": "uploads.tasks.clean_unused_media_task",
        "schedule": 86400.0,  # 하루에 한 번 실행
    },
    "check-system-health-every-hour": {
        "task": "config.tasks.check_system_health",
        "schedule": 3600.0,  # 1시간마다 실행
    },
}

# Redis 캐시
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# =================================================
# CKEditor 5 설정
# =================================================
# 컬러 팔레트
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

# 기본 설정
CKEDITOR_5_CUSTOM_CSS = "css/ckeditor_custom.css"
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "gif", "png", "pdf", "mp4", "mov"]
CKEDITOR_5_MAX_FILE_SIZE = 1024  # MB

# 에디터 구성
CKEDITOR_5_CONFIGS = {
    "default": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": {
            "items": [
                "heading",
                "|",
                "outdent",
                "indent",
                "alignment",
                "|",
                "bold",
                "italic",
                "link",
                "underline",
                "strikethrough",
                "code",
                "subscript",
                "superscript",
                "highlight",
                "|",
                "bulletedList",
                "numberedList",
                "todoList",
                "|",
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "removeFormat",
                "|",
                "codeBlock",
                "blockQuote",
                "mediaEmbed",
                "insertImage",
                "fileUpload",
                "insertTable",
                "|",
                "sourceEditing",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h2",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h3",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h4",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        },
    },
}

# =================================================
# 로깅 설정
# =================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "verbose",
            "level": "INFO",
        },
    },
    "loggers": {
        "uploads": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "homepage": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# 로깅 레벨 설정
LOGGING_LEVEL = env("LOGGING_LEVEL", default="INFO")
LOGGING["handlers"]["file"]["level"] = LOGGING_LEVEL
LOGGING["loggers"]["uploads"]["level"] = LOGGING_LEVEL
LOGGING["loggers"]["homepage"]["level"] = LOGGING_LEVEL
