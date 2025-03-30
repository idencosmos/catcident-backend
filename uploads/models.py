# uploads/models.py
# 미디어 파일 관리 및 해시 기반 중복 방지 시스템 구현
# Cloudflare R2 스토리지와 연동하여 파일 저장 및 관리
from django.db import models
import hashlib
from datetime import datetime


def generate_filename(instance, filename):
    """파일명을 날짜와 시간 기반으로 생성하여 중복 방지"""
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
        """파일 객체에서 SHA-256 해시 계산하여 중복 파일 식별에 사용"""
        sha256 = hashlib.sha256()
        if hasattr(file_obj, "chunks"):
            for chunk in file_obj.chunks():
                sha256.update(chunk)
        else:
            file_obj.seek(0)
            sha256.update(file_obj.read())
        return sha256.hexdigest()

    def _calculate_file_hash(self):
        """현재 인스턴스의 파일 해시값 계산"""
        return self.calculate_file_hash(self.file)

    def save(self, *args, **kwargs):
        # 파일이 존재하는지 확인
        if self.file:
            self.file.seek(0)

            # 파일 변경 여부 확인을 위한 변수
            old_file = None
            file_changed = False

            # 이미 저장된 객체인 경우(id가 있는 경우)
            if self.id:
                try:
                    # 기존 객체를 조회하여 파일이 변경되었는지 확인
                    old_obj = Media.objects.get(id=self.id)
                    if old_obj.file.name != self.file.name:
                        # 파일이 변경되었음을 표시하고 이전 파일 저장
                        file_changed = True
                        old_file = old_obj.file

                        # 파일이 변경되었으면 해시 재계산
                        self.hash_value = self._calculate_file_hash()
                        # 제목이 없으면 파일명으로 설정
                        if not self.title and hasattr(self.file, "name"):
                            self.title = self.file.file.name.split("/")[-1]
                except Media.DoesNotExist:
                    # 기존 객체가 없으면 새 해시 계산
                    self.hash_value = self._calculate_file_hash()
                    if not self.title and hasattr(self.file, "name"):
                        self.title = self.file.file.name.split("/")[-1]
            else:
                # 새 객체인 경우 해시 계산
                if not self.hash_value:  # 불필요한 재계산 방지
                    self.hash_value = self._calculate_file_hash()
                    if not self.title and hasattr(self.file, "name"):
                        self.title = self.file.file.name.split("/")[-1]

            # 중복 체크 (해시가 같은 다른 파일이 있는지)
            if (
                self.hash_value
                and Media.objects.filter(hash_value=self.hash_value)
                .exclude(id=self.id)
                .exists()
            ):
                # 중복 파일이 있는 경우, 기존 파일 사용하고 현재 업로드 중단
                existing_media = Media.objects.get(hash_value=self.hash_value)

                # 파일이 변경되었고 이전 파일이 있다면 삭제
                if file_changed and old_file and old_file.name:
                    try:
                        old_file.delete(
                            save=False
                        )  # 파일만 삭제하고 DB는 업데이트하지 않음
                    except Exception:
                        # 파일 삭제 실패해도 진행
                        pass

                self.id = existing_media.id
                return

            # 일반 저장 과정에서 파일이 변경되었다면 이전 파일 삭제
            if file_changed and old_file and old_file.name:
                try:
                    # 저장 전에 이전 파일 삭제
                    old_file.delete(save=False)
                except Exception:
                    # 파일 삭제 실패해도 진행
                    pass

        super().save(*args, **kwargs)

    def _check_usage(self):
        """모든 모델을 검사하여 현재 미디어 파일이 사용 중인지 확인"""
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
        """미디어 파일이 사용되는 모든 모델과 객체 정보 반환"""
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
