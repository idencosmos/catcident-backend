# homepage/models/gallery_models.py
# 갤러리 콘텐츠 관리 및 표시를 위한 모델을 정의합니다.

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media


class GalleryCategory(TranslatableModel):
    """갤러리 카테고리 모델"""

    slug = models.SlugField(unique=True, allow_unicode=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="카테고리 이름")
    )

    class Meta:
        verbose_name = "G01. Gallery Category"
        verbose_name_plural = "G01. Gallery Categories"

    def __str__(self):
        return (
            self.safe_translation_getter("name", any_language=True)
            or f"Category {self.pk}"
        )


class GalleryItem(TranslatableModel):
    """갤러리 아이템 모델"""

    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gallery_items",
    )
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_gallery_images",
        verbose_name="갤러리 이미지",
    )
    year = models.PositiveIntegerField(verbose_name="연도", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, verbose_name="메인 표시 여부")
    order = models.PositiveIntegerField(default=0, verbose_name="표시 순서")

    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="제목"),
        short_description=models.CharField(
            max_length=300, blank=True, null=True, verbose_name="간략한 설명"
        ),
        description=CKEditor5Field(
            "상세 설명", config_name="default", blank=True, null=True
        ),
    )

    class Meta:
        verbose_name = "G02. Gallery Item"
        verbose_name_plural = "G02. Gallery Items"
        ordering = ["order", "-year", "-created_at"]

    def __str__(self):
        return (
            self.safe_translation_getter("title", any_language=True)
            or f"Gallery Item {self.pk}"
        )
