# homepage/admin.py

from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import (
    # 기존 Global 모델
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
    # 기존 About 모델
    Creator,
    BookCategory,
    Book,
    Character,
    HistoryEvent,
    LicensePage,
    # 새로운 Resources 모델
    ResourceCategory,
    Resource,
    # 새로운 News 모델
    NewsCategory,
    News,
    # 새로운 Events 모델
    EventCategory,
    Event,
)


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

# =================== Resources Admin ===================

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Resource)
class ResourceAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "created_at")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

# =================== News Admin ===================

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "date", "created_at")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

# =================== Events Admin ===================

@admin.register(EventCategory)
class EventCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "date", "created_at")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)
