# uploads/models.py
from django.db import models
import hashlib
from datetime import datetime


def generate_filename(instance, filename):
    """파일명을 날짜 기반으로 생성"""
    ext = filename.split(".")[-1]  # 확장자 추출
    timestamp = datetime.now().strftime("%H%M%S")  # HHMMSS
    upload_path = f"{datetime.now().strftime('%Y/%m/%d')}-{timestamp}.{ext}"
    return upload_path


class Media(models.Model):
    file = models.FileField(upload_to=generate_filename)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        max_length=200, blank=True, null=True, help_text="파일의 표시 이름, 수정 가능"
    )
    is_used_cached = models.BooleanField(default=False, editable=False)
    hash_value = models.CharField(max_length=64, blank=True, null=True, unique=True)

    def __str__(self):
        return self.title or self.file.name

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"

    @staticmethod
    def calculate_file_hash(file_obj):
        """파일 객체에서 SHA-256 해시 계산"""
        sha256 = hashlib.sha256()
        if hasattr(file_obj, "chunks"):
            for chunk in file_obj.chunks():
                sha256.update(chunk)
        else:
            file_obj.seek(0)
            sha256.update(file_obj.read())
        return sha256.hexdigest()

    def _calculate_file_hash(self):
        return self.calculate_file_hash(self.file)

    def save(self, *args, **kwargs):
        if self.file and not self.hash_value:
            self.file.seek(0)
            self.hash_value = self._calculate_file_hash()
            if not self.title and hasattr(self.file, "name"):
                self.title = self.file.file.name.split("/")[-1]
            if (
                Media.objects.filter(hash_value=self.hash_value)
                .exclude(id=self.id)
                .exists()
            ):
                existing_media = Media.objects.get(hash_value=self.hash_value)
                self.id = existing_media.id
                return
        super().save(*args, **kwargs)

    def _check_usage(self):
        from django.apps import apps

        for model in apps.get_models():
            for field in model._meta.get_fields():
                if field.related_model == Media:
                    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                        if model.objects.filter(**{field.name: self}).exists():
                            return True
                    elif isinstance(field, models.ManyToManyField):
                        filter_kwargs = {f"{field.name}__id": self.id}
                        if model.objects.filter(**filter_kwargs).exists():
                            return True
        return False

    def get_usage_details(self):
        from django.apps import apps

        usage = []
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if field.related_model == Media:
                    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                        qs = model.objects.filter(**{field.name: self})
                        if qs.exists():
                            usage.append(
                                {
                                    "model": model._meta.verbose_name,
                                    "count": qs.count(),
                                    "objects": list(qs),
                                }
                            )
                    elif isinstance(field, models.ManyToManyField):
                        filter_kwargs = {f"{field.name}__id": self.id}
                        qs = model.objects.filter(**filter_kwargs)
                        if qs.exists():
                            usage.append(
                                {
                                    "model": model._meta.verbose_name,
                                    "count": qs.count(),
                                    "objects": list(qs),
                                }
                            )
        return usage
