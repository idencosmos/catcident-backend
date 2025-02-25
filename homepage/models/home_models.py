from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media


class HomeSection(TranslatableModel):
    SECTION_TYPES = (
        ("books", "New Books"),
        ("authors", "Authors"),
        ("news", "News"),
        ("events", "Events"),
        ("video", "Video"),
        ("custom", "Custom"),
    )
    LAYOUT_CHOICES = (
        ("full", "전체 너비"),
        ("half", "절반 너비"),
    )
    type = models.CharField(
        max_length=20, choices=SECTION_TYPES, unique=True, verbose_name="섹션 타입"
    )
    layout = models.CharField(
        max_length=20, choices=LAYOUT_CHOICES, default="full", verbose_name="레이아웃"
    )
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")
    order = models.PositiveIntegerField(verbose_name="표시 순서")

    translations = TranslatedFields(
        content=CKEditor5Field("내용", config_name="default", blank=True, null=True)
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "H01. 홈페이지 섹션"
        verbose_name_plural = "H01. 홈페이지 섹션들"

    def __str__(self):
        return f"{self.get_type_display()} (레이아웃: {self.layout}, 활성화: {self.is_active})"


class HeroSlide(TranslatableModel):
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_hero_slides",
        verbose_name="슬라이드 이미지",
    )
    link = models.URLField(blank=True, verbose_name="링크")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")
    order = models.PositiveIntegerField(verbose_name="표시 순서")

    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name="제목"),
        description=models.TextField(blank=True, verbose_name="설명"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "H02. Hero 슬라이드"
        verbose_name_plural = "H02. Hero 슬라이드들"

    def __str__(self):
        return (
            self.safe_translation_getter("title", any_language=True)
            or f"Slide {self.pk}"
        )
