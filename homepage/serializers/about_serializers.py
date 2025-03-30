# homepage/serializers/about_serializers.py
# About 페이지 관련 모델의 시리얼라이저 정의
# 책, 캐릭터, 크리에이터, 역사, 라이센스 정보를 API로 제공
from rest_framework import serializers
from homepage.models.about_models import (
    Creator,
    BookCategory,
    Book,
    Character,
    HistoryEvent,
    LicensePage,
)
from uploads.serializers import MediaSerializer


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    bio_summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo = MediaSerializer(read_only=True)

    class Meta:
        model = Creator
        fields = ["id", "slug", "photo", "name", "bio_summary", "description"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

    def get_bio_summary(self, obj):
        return obj.safe_translation_getter("bio_summary", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


# 간소화된 Creator 정보를 반환하는 시리얼라이저
class SimpleCreatorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


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
    summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = BookCategorySerializer(read_only=True)
    authors = SimpleCreatorSerializer(
        many=True, read_only=True
    )  # 간소화된 Creator 정보 사용
    cover_image = MediaSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "subtitle",
            "summary",
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

    def get_summary(self, obj):
        return obj.safe_translation_getter("summary", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class CharacterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    bio_summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    books = BookSerializer(many=True, read_only=True)
    creator = SimpleCreatorSerializer(read_only=True)  # 간소화된 Creator 정보 사용
    image = MediaSerializer(read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "slug",
            "image",
            "name",
            "bio_summary",
            "description",
            "books",
            "creator",
        ]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

    def get_bio_summary(self, obj):
        return obj.safe_translation_getter("bio_summary", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)


class HistoryEventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = MediaSerializer(read_only=True)

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
