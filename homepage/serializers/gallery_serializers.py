# homepage/serializers/gallery_serializers.py
# 갤러리 모델의 API 응답 형식을 정의합니다.

from rest_framework import serializers
from homepage.models.gallery_models import GalleryCategory, GalleryItem
from uploads.serializers import MediaSerializer


class GalleryCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = GalleryCategory
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


class GalleryItemListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    category = GalleryCategorySerializer(read_only=True)
    image = MediaSerializer(read_only=True)

    class Meta:
        model = GalleryItem
        fields = [
            "id",
            "title",
            "short_description",
            "image",
            "year",
            "category",
            "is_featured",
        ]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_short_description(self, obj):
        return obj.safe_translation_getter("short_description", any_language=True)


class GalleryItemDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = GalleryCategorySerializer(read_only=True)
    image = MediaSerializer(read_only=True)

    class Meta:
        model = GalleryItem
        fields = [
            "id",
            "title",
            "short_description",
            "description",
            "image",
            "year",
            "category",
            "is_featured",
        ]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_short_description(self, obj):
        return obj.safe_translation_getter("short_description", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)
