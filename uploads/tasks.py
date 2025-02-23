# uploads/tasks.py
from celery import shared_task
from .utils import clean_unused_media, update_media_usage


@shared_task
def clean_unused_media_task():
    """사용 여부 확인 후 미사용 미디어 삭제 (주기적 작업)"""
    clean_unused_media()  # 반환값 무시, 작업만 실행


@shared_task
def update_media_usage_async():
    """Admin에서 비동기로 사용 여부 업데이트"""
    return update_media_usage()


@shared_task
def clean_unused_media_async():
    """Admin에서 비동기로 사용 여부 확인 후 삭제"""
    return clean_unused_media()
