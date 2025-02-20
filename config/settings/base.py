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
    # 공통 앱
    "accounts",
    "homepage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# settings/base.py
R2_BUCKET_NAME = env("R2_BUCKET_NAME")
R2_REGION = env("R2_REGION", default="auto")
R2_ENDPOINT_URL = env("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY")

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
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "png", "pdf"]
CKEDITOR_5_MAX_FILE_SIZE = 10  # MB

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading",
                "|",
                "bold",
                "italic",
                "link",
                "bulletedList",
                "numberedList",
                "blockQuote",
                "imageUpload",
                "fileUpload",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "language": "en",
        # 테이블/이미지 등 추가 구성
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
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"],
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
    },
    "dark_theme": {
        # 다크모드용 Config 예시
        "toolbar": {
            "items": [
                "heading",
                "|",
                "bold",
                "italic",
                "link",
                "underline",
                "bulletedList",
                "numberedList",
                "blockQuote",
                "imageUpload",
                "fileUpload",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "language": "en",
        # 다크모드 시, content 영역에 다른 CSS를 적용하거나,
        # CKEDITOR_5_CUSTOM_CSS에서 다크 테마용 스타일을 함께 처리
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
        },
    },
}