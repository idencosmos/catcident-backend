# homepage/models/resources_models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media

class ResourceCategory(TranslatableModel):
    slug = models.SlugField(unique=True, allow_unicode=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="카테고리 이름")
    )

    class Meta:
        verbose_name = "R01. Resource Category"
        verbose_name_plural = "R01. Resource Categories"

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or f"Category {self.pk}"

class Resource(TranslatableModel):
    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources"
    )
    main_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_resource_main_images",
        verbose_name="메인 이미지"
    )
    file = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="homepage_resource_files",
        verbose_name="다운로드 파일"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="제목"),
        description=CKEditor5Field(
            "설명",
            config_name="default",
            blank=True,
            null=True
        )
    )

    class Meta:
        verbose_name = "R02. Resource"
        verbose_name_plural = "R02. Resources"

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or f"Resource {self.pk}"