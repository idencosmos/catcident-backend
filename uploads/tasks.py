# uploads/tasks.py
import logging
from celery import shared_task
from .utils import update_media_usage, clean_unused_media

logger = logging.getLogger(__name__)


@shared_task
def update_media_usage_async():
    """미디어 사용 여부를 비동기적으로 확인합니다."""
    try:
        updated_count = update_media_usage()
        logger.info(f"미디어 사용 여부 업데이트 완료: {updated_count}개 항목 업데이트")
        return {"status": "success", "updated_count": updated_count}
    except Exception as e:
        logger.error(f"미디어 사용 여부 업데이트 실패: {e}")
        return {"status": "error", "message": str(e)}


@shared_task
def clean_unused_media_async():
    """사용되지 않는 미디어 파일을 비동기적으로 정리합니다."""
    try:
        # 먼저 사용 여부 체크
        update_media_usage()
        # 미사용 파일 정리
        deleted_count = clean_unused_media()
        logger.info(f"미사용 미디어 정리 완료: {deleted_count}개 항목 삭제")
        return {"status": "success", "deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"미사용 미디어 정리 실패: {e}")
        return {"status": "error", "message": str(e)}


@shared_task
def clean_unused_media_task():
    """
    주기적으로 실행될 미디어 정리 태스크
    Celery Beat에 의해 스케줄링 됨
    """
    return clean_unused_media_async()
