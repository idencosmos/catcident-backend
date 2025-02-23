# uploads/signals.py
import importlib
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.apps import apps
from .models import Media
from .tasks import update_media_usage_async


def get_storage_class(storage_path):
    """주어진 경로에서 스토리지 클래스를 동적으로 임포트합니다."""
    module_name, class_name = storage_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def update_media_usage_cache(media):
    """주어진 Media 객체의 사용 상태를 비동기로 업데이트"""
    if media and isinstance(media, Media):
        update_media_usage_async.delay(media.id)


@receiver(pre_save)
def store_old_values(sender, instance, **kwargs):
    """저장 전 이전 ForeignKey/OneToOneField 값 저장"""
    if sender == Media:
        return
    for field in sender._meta.get_fields():
        if isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == Media:
            try:
                old_value = getattr(instance, field.name)
            except AttributeError:
                old_value = None
            setattr(instance, f"_old_{field.name}", old_value)


@receiver(post_save)
def update_media_references(sender, instance, **kwargs):
    """저장 후 Media 참조 상태 갱신"""
    if sender == Media:
        return
    for field in sender._meta.get_fields():
        if isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == Media:
            new_media = getattr(instance, field.name, None)
            old_media = getattr(instance, f"_old_{field.name}", None)
            update_media_usage_cache(new_media)
            if old_media and old_media != new_media:
                update_media_usage_cache(old_media)
        elif isinstance(field, models.ManyToManyField) and field.related_model == Media:
            related_manager = getattr(instance, field.name, None)
            if related_manager:
                for media in related_manager.all():
                    update_media_usage_cache(media)


@receiver(post_delete)
def update_media_references_on_delete(sender, instance, **kwargs):
    """삭제 후 Media 참조 상태 갱신 및 R2 파일 삭제"""
    if sender == Media:
        storage = get_storage_class(getattr(settings, "DEFAULT_FILE_STORAGE", ""))()
        if storage.exists(instance.file.name):
            storage.delete(instance.file.name)
        return
    for field in sender._meta.get_fields():
        if isinstance(field, (models.ForeignKey, models.OneToOneField)) and field.related_model == Media:
            media = getattr(instance, field.name, None)
            update_media_usage_cache(media)
        elif isinstance(field, models.ManyToManyField) and field.related_model == Media:
            related_manager = getattr(instance, field.name, None)
            if related_manager:
                for media in related_manager.all():
                    update_media_usage_cache(media)


@receiver(m2m_changed)
def handle_m2m_change(sender, instance, action, pk_set, **kwargs):
    """ManyToManyField 변경 시 Media 상태 갱신"""
    model = instance._meta.model
    for field in model._meta.get_fields():
        if isinstance(field, models.ManyToManyField) and field.related_model == Media:
            if sender == field.through and action in ['post_add', 'post_remove']:
                for pk in pk_set:
                    try:
                        media = Media.objects.get(pk=pk)
                        update_media_usage_cache(media)
                    except Media.DoesNotExist:
                        continue


def ready():
    """앱 초기화 시 모든 신호 연결"""
    from django.db.models import signals
    for model in apps.get_models():
        signals.pre_save.connect(store_old_values, sender=model)
        signals.post_save.connect(update_media_references, sender=model)
        signals.post_delete.connect(update_media_references_on_delete, sender=model)
        for field in model._meta.get_fields():
            if isinstance(field, models.ManyToManyField) and field.related_model == Media:
                signals.m2m_changed.connect(handle_m2m_change, sender=field.through)