# config/celery.py
import os
import environ

from celery import Celery

# 환경 변수 설정
env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 기본 .env 파일을 먼저 로드
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# DJANGO_ENV 값에 따라 .env.prod 또는 .env.dev 파일을 추가 로드
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
if DJANGO_ENV == 'production':
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
else:
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()