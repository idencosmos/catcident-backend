# uploads/models.py
from django.db import models
import hashlib


class Media(models.Model):
    file = models.FileField(upload_to='%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    is_used_cached = models.BooleanField(default=False, editable=False)  # 사용 여부 캐시
    hash_value = models.CharField(max_length=64, blank=True, null=True, unique=True)  # SHA-256 해시

    def __str__(self):
        return self.title or self.file.name

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"

    def save(self, *args, **kwargs):
        if self.file and not self.hash_value:
            self.file.seek(0)
            self.hash_value = self._calculate_file_hash()
            # 중복 체크: 동일 해시가 존재하면 저장하지 않음
            if Media.objects.filter(hash_value=self.hash_value).exclude(id=self.id).exists():
                existing_media = Media.objects.get(hash_value=self.hash_value)
                self.id = existing_media.id  # 기존 객체로 대체
                return
        super().save(*args, **kwargs)

    def _calculate_file_hash(self):
        """파일의 SHA-256 해시 계산"""
        sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def update_usage_cache(self):
        """Media 객체의 사용 여부를 계산하고 캐시 업데이트"""
        new_value = self._check_usage()
        if new_value != self.is_used_cached:
            self.is_used_cached = new_value
            self.save(update_fields=['is_used_cached'])
        return new_value

    def _check_usage(self):
        """이 Media 객체가 참조되고 있는지 확인"""
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
        """이 Media 객체의 사용처 상세 정보 반환"""
        from django.apps import apps
        usage = []
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if field.related_model == Media:
                    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                        qs = model.objects.filter(**{field.name: self})
                        if qs.exists():
                            usage.append({
                                'model': model._meta.verbose_name,
                                'count': qs.count(),
                                'objects': list(qs)
                            })
                    elif isinstance(field, models.ManyToManyField):
                        filter_kwargs = {f"{field.name}__id": self.id}
                        qs = model.objects.filter(**filter_kwargs)
                        if qs.exists():
                            usage.append({
                                'model': model._meta.verbose_name,
                                'count': qs.count(),
                                'objects': list(qs)
                            })
        return usage