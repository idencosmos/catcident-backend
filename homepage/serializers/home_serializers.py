from rest_framework import serializers
from uploads.serializers import MediaSerializer
from homepage.models import HomeSection, HeroSlide


class HomeSectionSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = HomeSection
        fields = ["id", "type", "layout", "is_active", "order", "content"]

    def get_content(self, obj):
        return obj.safe_translation_getter("content", any_language=True)


class HeroSlideSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = MediaSerializer(read_only=True)

    class Meta:
        model = HeroSlide
        fields = ["id", "image", "title", "description", "link", "is_active", "order"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter("description", any_language=True)
