# homepage/models/about_models.py
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from uploads.models import Media


class Creator(TranslatableModel):
    slug = models.SlugField(unique=True)
    photo = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="homepage_creator_photos",
    )

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        bio_summary=models.CharField(max_length=300, blank=True, null=True),
        description=CKEditor5Field(
            "Description", config_name="default", blank=True, null=True
        ),
    )

    def __str__(self):
        return (
            self.safe_translation_getter("name", any_language=True)
            or f"Creator {self.pk}"
        )

    class Meta:
        verbose_name = "A01. Creator"
        verbose_name_plural = "A01. Creators"


class BookCategory(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(max_length=100))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return (
            self.safe_translation_getter("name", any_language=True)
            or f"Category {self.pk}"
        )

    class Meta:
        verbose_name = "A02. Book Category"
        verbose_name_plural = "A02. Book Categories"


class Book(TranslatableModel):
    cover_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="homepage_book_covers",
    )
    pub_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey(
        BookCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="books",
    )
    authors = models.ManyToManyField(Creator, blank=True, related_name="books")

    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        subtitle=models.CharField(max_length=200, blank=True, null=True),
        description=CKEditor5Field(
            "Description", config_name="default", blank=True, null=True
        ),
    )

    def __str__(self):
        return (
            self.safe_translation_getter("title", any_language=True)
            or f"Book {self.pk}"
        )

    class Meta:
        verbose_name = "A03. Book"
        verbose_name_plural = "A03. Books"


class Character(TranslatableModel):
    slug = models.SlugField(unique=True)
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="homepage_character_images",
    )
    books = models.ManyToManyField(Book, blank=True, related_name="characters")
    creator = models.ForeignKey(
        Creator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="characters_created",
    )

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=CKEditor5Field(
            "Description", config_name="default", blank=True, null=True
        ),
    )

    def __str__(self):
        return (
            self.safe_translation_getter("name", any_language=True)
            or f"Character {self.pk}"
        )

    class Meta:
        verbose_name = "A04. Character"
        verbose_name_plural = "A04. Characters"


class HistoryEvent(TranslatableModel):
    date = models.DateField()
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="homepage_history_images",
    )

    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=CKEditor5Field(
            "Description", config_name="default", blank=True, null=True
        ),
    )

    class Meta:
        verbose_name = "A05. History Event"
        verbose_name_plural = "A05. History Events"
        ordering = ["date"]

    def __str__(self):
        return (
            self.safe_translation_getter("title", any_language=True)
            or f"Event {self.pk}"
        )


class LicensePage(TranslatableModel):
    updated_at = models.DateTimeField(default=timezone.now)

    translations = TranslatedFields(
        title=models.CharField(max_length=200, default="Licensing"),
        content=CKEditor5Field("Content", config_name="default", blank=True, null=True),
    )

    def save(self, *args, **kwargs):
        """항상 단일 인스턴스로 저장합니다."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """라이센스 페이지의 단일 인스턴스를 가져옵니다. 없으면 생성합니다."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True) or "LicensePage"

    class Meta:
        verbose_name = "A06. License Page"
        verbose_name_plural = "A06. License Pages"
