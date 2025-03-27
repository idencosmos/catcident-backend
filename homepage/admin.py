# homepage/admin.py
# Django 관리자 페이지 설정
# 다국어 콘텐츠 관리를 위한 모든 모델에 대한 관리자 인터페이스 정의

from django import forms
from django.db import models

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin, messages
from .signals import revalidate_nextjs_tag
from parler.admin import TranslatableAdmin, TranslatableTabularInline
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

# =================== Utility Functions ===================


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


revalidate_all_tags.short_description = "프론트엔드의 모든 Next.js 태그 재검증"

# =================== Mixin Classes ===================


class TranslatableFieldWidgetMixin:
    """
    Django-Parler 다국어 필드의 입력 위젯을 커스터마이징하는 믹스인
    사전 정의된 템플릿을 사용하여 필드 유형별 적절한 크기와 스타일을 적용합니다.
    """

    # 미리 정의된 필드 템플릿
    FIELD_TEMPLATES = {
        # 짧은 텍스트 필드용 (제목, 이름 등)
        "short_text": {"size": 60, "style": "width: calc(100% - 15px);"},
        # 중간 길이 텍스트 필드용 (요약, 짧은 설명 등)
        "medium_text": {"rows": 3, "cols": 60, "style": "width: calc(100% - 15px);"},
        # 긴 텍스트 필드용 (상세 설명, 컨텐츠 등)
        "long_text": {"rows": 6, "style": "width: calc(100% - 15px);"},
    }

    # 필드별 템플릿 지정 (각 Admin 클래스에서 오버라이드)
    field_widget_templates = {}

    def get_form(self, request, obj=None, **kwargs):
        """Admin 폼 생성 시 지정된 템플릿에 따라 필드 위젯 속성을 설정합니다."""
        form = super().get_form(request, obj, **kwargs)

        # 각 필드에 대해 지정된 템플릿 적용
        for field_name, template_name in self.field_widget_templates.items():
            if field_name in form.base_fields and template_name in self.FIELD_TEMPLATES:
                template = self.FIELD_TEMPLATES[template_name]

                # rows, cols가 있으면 Textarea 위젯으로 변경
                if "rows" in template and "cols" in template:
                    form.base_fields[field_name].widget = forms.Textarea(attrs=template)
                # 그 외에는 기존 위젯의 attrs 업데이트
                else:
                    form.base_fields[field_name].widget.attrs.update(template)

        return form


# =================== Global Admin ===================


@admin.register(SiteTitle)
class SiteTitleAdmin(TranslatableAdmin):
    list_display = ("title_display",)
    list_display_links = ("title_display",)

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)

    def has_add_permission(self, request):
        return not SiteTitle.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if SiteTitle.objects.exists():
            obj = SiteTitle.load()
            return HttpResponseRedirect(
                reverse(
                    f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                    args=(obj.pk,),
                )
            )
        return super().changelist_view(request, extra_context=extra_context)


class NavigationSubMenuInline(TranslatableTabularInline):
    model = NavigationSubMenu
    extra = 0
    fields = ("label", "href", "order")


class FooterSubMenuInline(TranslatableTabularInline):
    model = FooterSubMenu
    extra = 0
    fields = ("label", "href", "order")


@admin.register(NavigationGroup)
class NavigationGroupAdmin(TranslatableAdmin):
    list_display = ("id", "group_label_display", "highlighted", "order")
    list_editable = ("highlighted", "order")
    actions = [revalidate_all_tags]
    inlines = [NavigationSubMenuInline]

    def group_label_display(self, obj):
        return obj.safe_translation_getter("group_label", any_language=True)


@admin.register(FooterSection)
class FooterSectionAdmin(TranslatableAdmin):
    list_display = ("id", "label_display", "order")
    list_editable = ("order",)
    inlines = [FooterSubMenuInline]

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(FamilySite)
class FamilySiteAdmin(TranslatableAdmin):
    list_display = ("id", "label_display", "href", "order")
    list_editable = ("order",)

    def label_display(self, obj):
        return obj.safe_translation_getter("label", any_language=True)


@admin.register(Copyright)
class CopyrightAdmin(admin.ModelAdmin):
    list_display = ("text_display",)
    list_display_links = ("text_display",)

    def text_display(self, obj):
        if len(obj.text) > 100:
            return f"{obj.text[:100]}..."
        return obj.text or "저작권 정보 설정"

    def has_add_permission(self, request):
        return not Copyright.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if Copyright.objects.exists():
            obj = Copyright.load()
            return HttpResponseRedirect(
                reverse(
                    f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                    args=(obj.pk,),
                )
            )
        return super().changelist_view(request, extra_context=extra_context)


# =================== Home Admin ===================


@admin.register(HomeSection)
class HomeSectionAdmin(TranslatableAdmin):
    list_display = ("type", "get_type_display", "layout", "is_active", "order")
    list_editable = ("layout", "is_active", "order")
    list_filter = ("type", "layout", "is_active")
    search_fields = ("translations__content",)
    ordering = ("order",)
    actions = [revalidate_all_tags]

    def get_type_display(self, obj):
        return obj.get_type_display()

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
    list_display = ("title_display", "link", "is_active", "order")
    list_editable = ("link", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("translations__title", "translations__description")
    ordering = ("order",)
    actions = [revalidate_all_tags]

    def title_display(self, obj):
        return (
            obj.safe_translation_getter("title", any_language=True) or f"Slide {obj.pk}"
        )


# =================== About Admin ===================


@admin.register(Creator)
class CreatorAdmin(TranslatableFieldWidgetMixin, TranslatableAdmin):

    field_widget_templates = {
        "bio_summary": "medium_text",
    }

    list_display = ("id", "name_display", "slug")
    search_fields = ("translations__name", "translations__bio_summary", "slug")
    actions = [revalidate_all_tags]
    fieldsets = (
        (
            None,
            {
                "fields": ("slug", "photo"),
            },
        ),
        (
            "번역 가능 내용",
            {
                "fields": ("name", "bio_summary", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(BookCategory)
class BookCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "name_display", "slug")
    search_fields = ("translations__name", "slug")
    actions = [revalidate_all_tags]

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Book)
class BookAdmin(TranslatableFieldWidgetMixin, TranslatableAdmin):

    field_widget_templates = {
        "title": "short_text",
        "subtitle": "short_text",
    }

    list_display = ("id", "title_display", "subtitle_display", "category", "pub_date")
    list_filter = ("category", "pub_date")
    search_fields = (
        "translations__title",
        "translations__subtitle",
        "translations__description",
    )
    filter_horizontal = ("authors",)
    date_hierarchy = "pub_date"
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("category", "authors", "cover_image", "pub_date")}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "subtitle", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def title_display(self, obj):
        return (
            obj.safe_translation_getter("title", any_language=True) or f"Book {obj.pk}"
        )

    def subtitle_display(self, obj):
        return obj.safe_translation_getter("subtitle", any_language=True) or "-"


@admin.register(Character)
class CharacterAdmin(TranslatableAdmin):
    list_display = ("id", "name_display", "slug")
    search_fields = ("translations__name", "translations__description", "slug")
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("slug", "image", "books", "creator")}),
        (
            "번역 가능 내용",
            {
                "fields": ("name", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def name_display(self, obj):
        return (
            obj.safe_translation_getter("name", any_language=True)
            or f"Character {obj.pk}"
        )


@admin.register(HistoryEvent)
class HistoryEventAdmin(TranslatableAdmin):
    list_display = ("id", "date", "title_display")
    list_filter = ("date",)
    search_fields = ("translations__title", "translations__description")
    ordering = ("date",)
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("date", "image")}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def title_display(self, obj):
        return (
            obj.safe_translation_getter("title", any_language=True) or f"Event {obj.pk}"
        )


@admin.register(LicensePage)
class LicensePageAdmin(TranslatableAdmin):
    list_display = ("title_display", "updated_at")
    list_display_links = ("title_display",)
    readonly_fields = ("updated_at",)
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("updated_at",)}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "content"),
                "description": "여러 언어로 번역 가능한 라이센스 정보입니다.",
            },
        ),
    )

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True) or "라이센스"

    def has_add_permission(self, request):
        """라이센스 페이지가 없는 경우에만 추가를 허용합니다."""
        return not LicensePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """라이센스 페이지는 삭제할 수 없습니다."""
        return False

    def changelist_view(self, request, extra_context=None):
        """
        라이센스 페이지가 이미 존재하는 경우 해당 객체의 수정 페이지로 바로 리디렉션합니다.
        """
        if LicensePage.objects.exists():
            obj = LicensePage.load()
            return HttpResponseRedirect(
                reverse(
                    f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                    args=(obj.pk,),
                )
            )
        return super().changelist_view(request, extra_context=extra_context)


# =================== Resource Admin ===================


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")
    search_fields = ("translations__name", "slug")
    actions = [revalidate_all_tags]

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Resource)
class ResourceAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("translations__title", "translations__description")
    readonly_fields = ("created_at",)
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("category", "main_image", "file", "created_at")}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def title_display(self, obj):
        return (
            obj.safe_translation_getter("title", any_language=True)
            or f"Resource {obj.pk}"
        )


# =================== News Admin ===================


@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")
    search_fields = ("translations__name", "slug")
    actions = [revalidate_all_tags]

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "title_display",
        "category",
        "date",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "date")
    search_fields = ("translations__title", "translations__content")
    date_hierarchy = "date"
    readonly_fields = ("created_at", "updated_at")
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("category", "main_image", "date")}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "content"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
        (
            "시스템 정보",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)


# =================== Event Admin ===================


@admin.register(EventCategory)
class EventCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")
    search_fields = ("translations__name", "slug")
    actions = [revalidate_all_tags]

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = ("id", "title_display", "category", "date", "created_at")
    list_filter = ("category", "date")
    search_fields = ("translations__title", "translations__description")
    date_hierarchy = "date"
    readonly_fields = ("created_at",)
    actions = [revalidate_all_tags]
    fieldsets = (
        (None, {"fields": ("category", "main_image", "date")}),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
        ("시스템 정보", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def title_display(self, obj):
        return obj.safe_translation_getter("title", any_language=True)


# =================== Gallery Admin ===================


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "slug", "name_display")
    search_fields = ("translations__name", "slug")
    actions = [revalidate_all_tags]

    def name_display(self, obj):
        return obj.safe_translation_getter("name", any_language=True)


@admin.register(GalleryItem)
class GalleryItemAdmin(TranslatableFieldWidgetMixin, TranslatableAdmin):
    field_widget_templates = {
        "title": "short_text",
        "short_description": "medium_text",
    }

    list_display = (
        "id",
        "title_display",
        "category",
        "year",
        "is_featured",
        "order",
        "created_at",
    )
    list_filter = ("category", "year", "is_featured", "created_at")
    list_editable = ("is_featured", "order")
    search_fields = (
        "translations__title",
        "translations__short_description",
        "translations__description",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category",
                    "image",
                    "year",
                    "is_featured",
                    "order",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "번역 가능 내용",
            {
                "fields": ("title", "short_description", "description"),
                "description": "여러 언어로 번역 가능한 컨텐츠입니다.",
            },
        ),
    )

    def title_display(self, obj):
        return (
            obj.safe_translation_getter("title", any_language=True)
            or f"Gallery Item {obj.pk}"
        )
