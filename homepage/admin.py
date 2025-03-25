# homepage/admin.py

from django.contrib import admin, messages
from .signals import revalidate_nextjs_tag
from parler.admin import TranslatableAdmin
from .models import (
    # Global 모델
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
    # Home 모델
    HomeSection,
    HeroSlide,
    # About 모델
    Creator,
    BookCategory,
    Book,
    Character,
    HistoryEvent,
    LicensePage,
    # Resources 모델
    ResourceCategory,
    Resource,
    # News 모델
    NewsCategory,
    News,
    # Events 모델
    EventCategory,
    Event,
    # Gallery 모델
    GalleryCategory,
    GalleryItem,
)


def revalidate_all_tags(modeladmin, request, queryset):
    """모든 Next.js 태그를 재검증합니다"""
    # 글로벌 태그
    global_tags = [
        "global",
        "sitetitle",
        "navigation",
        "footer",
        "familysite",
        "copyright",
    ]
    # 섹션별 태그
    section_tags = ["home", "about", "news", "events", "gallery"]
    # 컨텐츠 태그
    content_tags = [
        "homesections",
        "heroslides",
        "newscategories",
        "eventcategories",
        "creators",
        "books",
        "bookcategories",
        "characters",
        "history",
        "license",
        "gallerycategories",
        "galleryitems",
    ]

    # 모든 태그 재검증
    total_tags = global_tags + section_tags + content_tags
    for tag in total_tags:
        revalidate_nextjs_tag(tag)

    messages.success(
        request, f"총 {len(total_tags)}개의 Next.js 태그가 성공적으로 재검증되었습니다."
    )


revalidate_all_tags.short_description = "모든 Next.js 태그 재검증"


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
    actions = [revalidate_all_tags]


# =================== Home Admin ===================


@admin.register(HomeSection)
class HomeSectionAdmin(TranslatableAdmin):
    list_display = ("type", "layout", "is_active", "order")
    list_editable = ("layout", "is_active", "order")
    list_filter = ("type", "is_active")
    ordering = ("order",)

    fieldsets = (
        (
            None,
            {
                "fields": ("type", "layout", "is_active", "order"),
            },
        ),
        (
            "Custom 콘텐츠",
            {
                "fields": ("content",),
                "description": "'Custom' 타입 섹션에서만 사용됩니다.",
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.type != "custom":
            return fieldsets[:-1]  # 'custom'이 아닌 경우 content 필드 숨김
        return fieldsets


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslatableAdmin):
    list_display = ("title_display", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    ordering = ("order",)

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)


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


# =================== Resource Admin ===================


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


# =================== Event Admin ===================


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


# =================== Gallery Admin ===================


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(GalleryItem)
class GalleryItemAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "year", "is_featured", "order")
    list_filter = ("category", "year", "is_featured")
    list_editable = ("is_featured", "order")
    search_fields = ("translations__title", "translations__short_description")

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)
