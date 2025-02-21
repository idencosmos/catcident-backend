# uploads/storages.py
import os
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class BaseR2Storage(S3Boto3Storage):
    """R2 공통 설정을 위한 기본 클래스"""
    def __init__(self, *args, **kwargs):
        kwargs["bucket_name"] = getattr(settings, "R2_BUCKET_NAME", "")
        kwargs["region_name"] = getattr(settings, "R2_REGION", "auto")
        kwargs["endpoint_url"] = getattr(settings, "R2_ENDPOINT_URL", "")
        kwargs["access_key"] = getattr(settings, "R2_ACCESS_KEY_ID", "")
        kwargs["secret_key"] = getattr(settings, "R2_SECRET_ACCESS_KEY", "")
        kwargs["file_overwrite"] = False
        super().__init__(*args, **kwargs)


class StaticStorage(BaseR2Storage):
    """정적 파일용 스토리지 (/static/)"""
    location = "static"


class MediaStorage(BaseR2Storage):
    """미디어 파일용 스토리지 (/media/)"""
    location = "media"


class CKEditor5Storage(BaseR2Storage):
    """CKEditor5 업로드용 스토리지 (/uploads/)"""
    location = "uploads"