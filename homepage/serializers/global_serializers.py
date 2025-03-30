# homepage/serializers/global_serializers.py
from rest_framework import serializers

from homepage.models.global_models import (
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
)


class SiteTitleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = SiteTitle
        fields = ["id", "title"]

    def get_title(self, obj):
        # LocaleMiddleware가 설정한 현재 언어의 title
        return obj.safe_translation_getter("title", any_language=True)


class NavigationSubMenuSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = NavigationSubMenu
        fields = ["id", "href", "label"]

    def get_label(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


class NavigationGroupSerializer(serializers.ModelSerializer):
    group_label = serializers.SerializerMethodField()
    sub_menus = NavigationSubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = NavigationGroup
        fields = ["id", "group_label", "highlighted", "sub_menus"]

    def get_group_label(self, obj):
        return obj.safe_translation_getter("group_label", any_language=True)


class FooterSubMenuSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = FooterSubMenu
        fields = ["id", "href", "label", "open_in_new_tab"]

    def get_label(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


class FooterSectionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    sub_menus = FooterSubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = FooterSection
        fields = ["id", "label", "sub_menus"]

    def get_label(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


class FamilySiteSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = FamilySite
        fields = ["id", "href", "label"]

    def get_label(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


class CopyrightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copyright
        fields = ["id", "text"]
