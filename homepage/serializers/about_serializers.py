# homepage/serializers/about_serializers.py

from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from homepage.models.about_models import (
    Creator,
    BookCategory, Book,
    Character, HistoryEvent,
    LicensePage
)

class CreatorSerializer(TranslatableModelSerializer):
    """
    CreatorPageBlock 대신 Creator 모델 자체에
    'description'을 포함시켰으므로 page_blocks 제거.
    """
    translations = TranslatedFieldsField(shared_model=Creator)
    
    class Meta:
        model = Creator
        fields = [
            "id",
            "slug",
            "photo",
            "translations",  # name, bio_summary, description
        ]


class BookCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BookCategory)

    class Meta:
        model = BookCategory
        fields = [
            "id", "slug", "translations"
        ]


class BookSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Book)
    category = BookCategorySerializer(read_only=True)
    # authors → CreatorSerializer 중첩
    authors = CreatorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "translations",  # title, subtitle, description
            "cover_image", "pub_date", "category", "authors",
        ]


class CharacterSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Character)
    books = BookSerializer(many=True, read_only=True)
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = Character
        fields = [
            "id", "slug", "image",
            "translations",  # name, description
            "books", "creator",
        ]


class HistoryEventSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=HistoryEvent)

    class Meta:
        model = HistoryEvent
        fields = [
            "id", "date", "image",
            "translations",  # title, description
        ]


class LicensePageSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=LicensePage)

    class Meta:
        model = LicensePage
        fields = [
            "id", "updated_at",
            "translations",  # title, content
        ]
