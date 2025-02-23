# uploads/tasks.py
from celery import shared_task
from .models import Media


@shared_task
def update_media_usage_async(media_id):
    """비동기로 Media 객체의 사용 상태 업데이트"""
    try:
        media = Media.objects.get(id=media_id)
        media.update_usage_cache()
    except Media.DoesNotExist:
        pass  # 존재하지 않는 경우 무시

# uploads/tasks.py에 추가
@shared_task
def clean_unused_media_task():
    from uploads.models import Media
    unused = Media.objects.filter(is_used_cached=False)
    unused.delete()