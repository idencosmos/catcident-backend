# homepage/serializers/about_serializers.py

from rest_framework import serializers
from homepage.models.about_models import (
    Creator,
    BookCategory,
    Book,
    Character,
    HistoryEvent,
    LicensePage,
)


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    bio_summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    # slug, photo는 원본 필드 그대로

    class Meta:
        model = Creator
        fields = ["id", "slug", "photo", "name", "bio_summary", "description"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

    def get_bio_summary(self, obj):
        return obj.safe_translation_getter("bio_summary", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class BookCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = BookCategory
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


class BookSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = BookCategorySerializer(read_only=True)
    # authors: CreatorSerializer 중첩

    authors = CreatorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "cover_image",
            "pub_date",
            "category",
            "authors",
        ]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_subtitle(self, obj):
        return obj.safe_translation_getter("subtitle", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class CharacterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    books = BookSerializer(many=True, read_only=True)
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "slug",
            "image",
            "name",
            "description",
            "books",
            "creator",
        ]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class HistoryEventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = HistoryEvent
        fields = ["id", "date", "image", "title", "description"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class LicensePageSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = LicensePage
        fields = ["id", "updated_at", "title", "content"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_content(self, obj):
        return obj.safe_translation_getter("content", any_language=True)
