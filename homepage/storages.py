# myproject/storages.py

import os
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class CloudflareR2Storage(S3Boto3Storage):
    """
    Django-Storages S3Boto3 기반으로,
    Cloudflare R2에 파일을 업로드하기 위한 스토리지 클래스.
    """
    def __init__(self, *args, **kwargs):
        # kwargs에 원하는 region_name, endpoint_url, access_key 등 주입
        kwargs["bucket_name"] = getattr(settings, "R2_BUCKET_NAME", "")
        kwargs["region_name"] = getattr(settings, "R2_REGION", "auto")  # R2 region이 'auto'일 수도 있음
        kwargs["endpoint_url"] = getattr(settings, "R2_ENDPOINT_URL", "")
        kwargs["access_key"] = getattr(settings, "R2_ACCESS_KEY_ID", "")
        kwargs["secret_key"] = getattr(settings, "R2_SECRET_ACCESS_KEY", "")
        # file_overwrite=False -> 동일 파일명 업로드 시 중복 처리
        kwargs["file_overwrite"] = False
        # ACL, signature_version 등도 필요 시 설정
        super().__init__(*args, **kwargs)
