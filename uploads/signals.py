from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Media
import logging

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Media)
def update_media_references_on_delete(sender, instance, **kwargs):
    try:
        default_storage.delete(instance.file.name)
    except Exception as e:
        logger.warning(f"Failed to delete file {instance.file.name}: {e}")
