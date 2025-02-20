from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from homepage.models.global_models import (
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
)

class NavigationSubMenuSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=NavigationSubMenu)

    class Meta:
        model = NavigationSubMenu
        fields = [
            "id", "href", "translations"
        ]


class NavigationGroupSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=NavigationGroup)
    sub_menus = NavigationSubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = NavigationGroup
        fields = [
            "id", "translations",  # group_label
            "highlighted",
            "sub_menus",
        ]


class FooterSubMenuSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=FooterSubMenu)

    class Meta:
        model = FooterSubMenu
        fields = [
            "id", "href", "translations"
        ]


class FooterSectionSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=FooterSection)
    sub_menus = FooterSubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = FooterSection
        fields = [
            "id", "translations",
            "sub_menus",
        ]


class SiteTitleSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteTitle)

    class Meta:
        model = SiteTitle
        fields = [
            "id", "translations"
        ]


class FamilySiteSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=FamilySite)

    class Meta:
        model = FamilySite
        fields = [
            "id", "href", "translations"
        ]


class CopyrightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copyright
        fields = [
            "id", "text"
        ]
