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

    def url(self, name):
        public_domain = getattr(settings, "MEDIA_PUBLIC_DOMAIN")
        return f"{public_domain}/static/{name}"


class MediaStorage(BaseR2Storage):
    """미디어 파일용 스토리지 (/media/)"""

    location = "media"

    def url(self, name):
        public_domain = getattr(settings, "MEDIA_PUBLIC_DOMAIN")
        # Media 객체에서 해당 파일의 해시값 가져오기
        try:
            # 상대 경로(name)로 Media 객체 필터링
            from uploads.models import Media

            media = Media.objects.filter(file=name).first()
            hash_param = (
                f"?v={media.hash_value[:8]}" if media and media.hash_value else ""
            )
        except Exception:
            hash_param = ""
        return f"{public_domain}/media/{name}{hash_param}"

    def _save(self, name, content):
        name = super()._save(name, content)
        # 캐시 헤더 설정
        params = {
            "ContentType": self.get_object_parameters(name).get("ContentType", ""),
            "CacheControl": "public, max-age=31536000, immutable",
        }
        self.connection.meta.client.copy_object(
            CopySource={"Bucket": self.bucket_name, "Key": self.location + "/" + name},
            Bucket=self.bucket_name,
            Key=self.location + "/" + name,
            MetadataDirective="REPLACE",
            **params,
        )
        return name
