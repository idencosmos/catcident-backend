# homepage/serializers/news_serializers.py
from rest_framework import serializers
from homepage.models.news_models import NewsCategory, News
from uploads.serializers import MediaSerializer

class NewsCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = NewsCategory
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        return obj.safe_translation_getter("name", any_language=True)

class NewsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    category = NewsCategorySerializer(read_only=True)
    main_image = MediaSerializer(read_only=True)

    class Meta:
        model = News
        fields = ["id", "title", "content", "category", "main_image", "date", "created_at"]

    def get_title(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def get_content(self, obj):
        return obj.safe_translation_getter("content", any_language=True)