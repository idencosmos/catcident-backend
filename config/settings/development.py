from .base import *

DEBUG = True

ALLOWED_HOSTS = ["api.catcident.local", "catcident-backend-api-1"]
CSRF_TRUSTED_ORIGINS = ["https://api.catcident.local"]
CORS_ALLOWED_ORIGINS = [
    "https://catcident.local",
    "https://cdn.catcident.com",
    "http://catcident-frontend-web-1:3000",
]

# Debug Toolbar
INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

# SSL Proxy (Caddy) 설정
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False

LOGGING["handlers"]["console"] = {
    "class": "logging.StreamHandler",
    "formatter": "verbose",
    "level": "DEBUG",
}
LOGGING["loggers"]["uploads"]["handlers"] = ["console", "file"]
LOGGING["loggers"]["uploads"]["level"] = "DEBUG"
