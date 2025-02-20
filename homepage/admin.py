# homepage/admin.py

from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import (
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
)
from .models import Creator, BookCategory, Book, Character, HistoryEvent, LicensePage


@admin.register(SiteTitle)
class SiteTitleAdmin(TranslatableAdmin):
    list_display = ("id", "title_display")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)


@admin.register(NavigationGroup)
class NavigationGroupAdmin(TranslatableAdmin):
    list_display = ("id", "group_label_display", "highlighted")

    def group_label_display(self, obj):
        return obj.safe_translation_getter("group_label", any_language=True)


@admin.register(NavigationSubMenu)
class NavigationSubMenuAdmin(TranslatableAdmin):
    list_display = ("id", "parent_group", "label_display", "href")

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(FooterSection)
class FooterSectionAdmin(TranslatableAdmin):
    list_display = ("id", "label_display")

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(FooterSubMenu)
class FooterSubMenuAdmin(TranslatableAdmin):
    list_display = ("id", "footer_section", "label_display", "href")

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(FamilySite)
class FamilySiteAdmin(TranslatableAdmin):
    list_display = ("id", "label_display", "href")

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(Copyright)
class CopyrightAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


# =================== About Admin ===================


@admin.register(Creator)
class CreatorAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(BookCategory)
class BookCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "name_display", "slug")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Book)
class BookAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "subtitle_display", "category", "pub_date")
    filter_horizontal = ("authors",)

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def subtitle_display(self, obj):
        return obj.safe_translation_getter("subtitle", any_language=True)


@admin.register(Character)
class CharacterAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(HistoryEvent)
class HistoryEventAdmin(TranslatableAdmin):
    list_display = ("id", "date", "title_display")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)


@admin.register(LicensePage)
class LicensePageAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "updated_at")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)
