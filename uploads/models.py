# uploads/models.py
from django.db import models


class Media(models.Model):
    file = models.FileField(upload_to='%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    is_used_cached = models.BooleanField(default=False, editable=False)  # 사용 여부 캐시

    def __str__(self):
        return self.title or self.file.name

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"

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