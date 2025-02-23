# uploads/utils.py
from django.apps import apps
from django_ckeditor_5.fields import CKEditor5Field
from urllib.parse import urlparse
from .models import Media
from parler.models import TranslatableModel
import re


def update_media_usage():
    """모든 미디어의 사용 여부를 확인하고 업데이트합니다."""
    used_paths = set()
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if isinstance(field, CKEditor5Field):
                for instance in model.objects.all():
                    if isinstance(instance, TranslatableModel):
                        # TranslatableModel인 경우 translations를 순회
                        for translation in instance.translations.all():
                            content = getattr(translation, field.name, "")
                            if content:
                                url_pattern = re.compile(r'src=["\']([^"\']+)["\']')
                                urls = url_pattern.findall(content)
                                for url in urls:
                                    parsed = urlparse(url)
                                    path = parsed.path
                                    used_paths.add(path)
                    else:
                        # 번역 모델이거나 일반 모델인 경우 직접 필드 확인
                        content = getattr(instance, field.name, "")
                        if content:
                            url_pattern = re.compile(r'src=["\']([^"\']+)["\']')
                            urls = url_pattern.findall(content)
                            for url in urls:
                                parsed = urlparse(url)
                                path = parsed.path
                                used_paths.add(path)
    all_media = Media.objects.all()
    updated_count = 0
    for media in all_media:
        media_path = urlparse(media.file.url).path
        is_used = media_path in used_paths or media._check_usage()
        if is_used != media.is_used_cached:
            media.is_used_cached = is_used
            media.save(update_fields=["is_used_cached"])
            updated_count += 1
    return updated_count


def clean_unused_media():
    """사용 여부를 확인한 후 미사용 미디어를 삭제합니다."""
    updated_count = update_media_usage()
    unused = Media.objects.filter(is_used_cached=False)
    count, _ = unused.delete()
    return updated_count, count
