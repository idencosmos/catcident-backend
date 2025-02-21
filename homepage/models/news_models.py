# homepage/models/news_models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media

class NewsCategory(TranslatableModel):
    slug = models.SlugField(unique=True, allow_unicode=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="카테고리 이름")
    )

    class Meta:
        verbose_name = "N01. News Category"
        verbose_name_plural = "N01. News Categories"

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or f"Category {self.pk}"

class News(TranslatableModel):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news"
    )
    main_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_news_main_images",
        verbose_name="메인 이미지"
    )
    date = models.DateField(verbose_name="게시 날짜")
    created_at = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="제목"),
        content=CKEditor5Field(
            "내용",
            config_name="default",
            blank=True,
            null=True
        )
    )

    class Meta:
        verbose_name = "N02. News"
        verbose_name_plural = "N02. News"

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or f"News {self.pk}"