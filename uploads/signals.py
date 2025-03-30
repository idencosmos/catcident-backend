# 미디어 파일 삭제 시 R2 스토리지에서 실제 파일도 함께 삭제하는 시그널 처리
# post_delete 이벤트 감지 및 처리
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Media
import logging

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Media)
def delete_media_file_on_delete(sender, instance, **kwargs):
    """
    Media 모델 인스턴스가 삭제될 때 연결된 파일을 R2 스토리지에서 삭제합니다.
    두 가지 방법으로 삭제를 시도하며, 첫 번째 방법 실패 시 두 번째 방법을 시도합니다.
    """
    if not instance.file:
        return

    file_name = instance.file.name

    try:
        # 방법 1: FileField의 delete 메서드 사용
        instance.file.delete(save=False)
        logger.info(f"파일 삭제 성공(file.delete): {file_name}")
        return
    except Exception as e:
        logger.warning(f"파일 삭제 실패(file.delete): {file_name} - {e}")

        # 방법 2: 스토리지 API 직접 사용
        try:
            default_storage.delete(file_name)
            logger.info(f"파일 삭제 성공(default_storage): {file_name}")
        except Exception as e2:
            logger.error(f"모든 파일 삭제 시도 실패: {file_name} - {e2}")
