# config/settings/base.py

import environ
from pathlib import Path

# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))  # Default value for DEBUG is False

environ.Env.read_env()  # reading .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "corsheaders",
    "django_ckeditor_5",
    "parler",
    "storages",
    "django_celery_beat",
    # 공통 앱
    "accounts",
    "homepage",
    "uploads",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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

# CORS 허용
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

PARLER_LANGUAGES = {
    None: (  # Default site
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

LANGUAGE_CODE = "ko"  # 기본 언어
LANGUAGES = (
    ("ko", "Korean"),
    ("en", "English"),
    # 필요하면 추가 언어
)

# R2 설정
R2_BUCKET_NAME = env("R2_BUCKET_NAME")
R2_REGION = env("R2_REGION", default="auto")
R2_ENDPOINT_URL = env("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static files
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = "staticfiles"

# Media files
MEDIA_URL = env("MEDIA_URL", default="/media/")
DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")
MEDIA_ROOT = "media"


STORAGES = {
    "staticfiles": {"BACKEND": env("STATICFILES_STORAGE")},
    "default": {"BACKEND": env("DEFAULT_FILE_STORAGE")},
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF 기본 설정(필요 시)
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # 필요하다면 추가
}

# Celery 설정
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"

# Redis 캐시 설정
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BEAT_SCHEDULE = {
    'clean-unused-media-every-day': {
        'task': 'uploads.tasks.clean_unused_media_task',
        'schedule': 864000.0,  # 240시간마다
    },
}

# CKEditor 5 Settings
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

# (1) CKEditor 5 커스텀 CSS
# 아래처럼 Admin 등에서 로드될 추가 CSS 파일 경로 지정 가능
CKEDITOR_5_CUSTOM_CSS = "css/ckeditor_custom.css"
# → 이 파일은 staticfiles 디렉토리(예: myapp/static/css/ckeditor_custom.css)에 있어야 함
#   collectstatic 후 /static/css/ckeditor_custom.css 로 배포됨

# (2) CKEditor 5 파일 저장소(Cloudflare R2 설정과 연동)
CKEDITOR_5_FILE_STORAGE = env("CKEDITOR_5_FILE_STORAGE")

# (Optional) 사용자 인증 필요 정도 (any/authenticated/staff)
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

# (Optional) 허용할 파일 타입
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "gif", "png", "pdf"]
CKEDITOR_5_MAX_FILE_SIZE = 10  # MB

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
