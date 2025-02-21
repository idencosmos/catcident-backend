# homepage/models/events_models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media

class EventCategory(TranslatableModel):
    slug = models.SlugField(unique=True, allow_unicode=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="카테고리 이름")
    )

    class Meta:
        verbose_name = "E01. Event Category"
        verbose_name_plural = "E01. Event Categories"

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or f"Category {self.pk}"

class Event(TranslatableModel):
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )
    main_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_event_main_images",
        verbose_name="메인 이미지"
    )
    date = models.DateField(verbose_name="행사 날짜")
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
        verbose_name = "E02. Event"
        verbose_name_plural = "E02. Events"

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or f"Event {self.pk}"