"""
/homepage/signals.py
모델 변경 이벤트를 감지하여 Next.js 캐시 태그 재검증 시그널 정의
Django 모델 변경 시 프론트엔드 캐시를 자동 갱신하기 위한 시그널 핸들러 구현
"""

import logging
import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models.global_models import (
    SiteTitle,
    NavigationGroup,
    NavigationSubMenu,
    FooterSection,
    FooterSubMenu,
    FamilySite,
    Copyright,
)
from .models.news_models import NewsCategory, News
from .models.event_models import EventCategory, Event
from .models.about_models import (
    Creator,
    BookCategory,
    Book,
    Character,
    HistoryEvent,
    LicensePage,
)
from .models.home_models import HomeSection, HeroSlide
from .models.gallery_models import GalleryCategory, GalleryItem

logger = logging.getLogger(__name__)


# 태그 카테고리 정의
GLOBAL_TAGS = [
    "global",
    "sitetitle",
    "navigation",
    "footer",
    "familysite",
    "copyright",
]

SECTION_TAGS = ["home", "about", "news", "events", "gallery"]

CONTENT_TAGS = [
    "homesections",
    "heroslides",
    "newscategories",
    "eventcategories",
    "creators",
    "books",
    "bookcategories",
    "characters",
    "history",
    "licenses",
    "gallerycategories",
    "galleryitems",
]

# 모든 태그 목록 (재검증시 사용)
ALL_TAGS = GLOBAL_TAGS + SECTION_TAGS + CONTENT_TAGS


def revalidate_nextjs_tag(tag):
    """
    Next.js 개별 태그 재검증 요청 함수
    태그명을 받아 Next.js API 엔드포인트로 재검증 요청을 전송합니다.
    """
    nextjs_revalidate_url = getattr(settings, "NEXTJS_REVALIDATE_URL", None)
    nextjs_revalidate_token = getattr(settings, "NEXTJS_REVALIDATE_TOKEN", None)

    if not nextjs_revalidate_url or not nextjs_revalidate_token:
        logger.warning(
            "NEXTJS_REVALIDATE_URL 또는 NEXTJS_REVALIDATE_TOKEN 설정이 없습니다"
        )
        return

    try:
        response = requests.post(
            nextjs_revalidate_url,
            json={"tag": tag},
            headers={"Authorization": f"Bearer {nextjs_revalidate_token}"},
        )
        if response.status_code == 200:
            logger.info(f"태그 재검증 성공: {tag}")
        else:
            logger.error(
                f"태그 재검증 실패: {tag}, 상태 코드: {response.status_code}, 응답: {response.text}"
            )
    except Exception as e:
        logger.error(f"Next.js 재검증 API 호출 오류: {e}")


def revalidate_all_nextjs_tags():
    """
    모든 Next.js 태그를 재검증하는 함수
    모든 정의된 태그에 대해 재검증 요청을 보내고 총 개수를 반환합니다.
    """
    tag_count = 0
    for tag in ALL_TAGS:
        revalidate_nextjs_tag(tag)
        tag_count += 1

    return tag_count


# Global models signals
@receiver(post_save, sender=SiteTitle)
@receiver(post_delete, sender=SiteTitle)
def handle_sitetitle_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("sitetitle")


@receiver(post_save, sender=NavigationGroup)
@receiver(post_delete, sender=NavigationGroup)
def handle_navigation_group_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("navigation")


@receiver(post_save, sender=NavigationSubMenu)
@receiver(post_delete, sender=NavigationSubMenu)
def handle_navigation_submenu_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("navigation")


@receiver(post_save, sender=FooterSection)
@receiver(post_delete, sender=FooterSection)
def handle_footer_section_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("footer")


@receiver(post_save, sender=FooterSubMenu)
@receiver(post_delete, sender=FooterSubMenu)
def handle_footer_submenu_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("footer")


@receiver(post_save, sender=FamilySite)
@receiver(post_delete, sender=FamilySite)
def handle_familysite_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("familysite")


@receiver(post_save, sender=Copyright)
@receiver(post_delete, sender=Copyright)
def handle_copyright_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("global")
    revalidate_nextjs_tag("copyright")


# News models signals
@receiver(post_save, sender=NewsCategory)
@receiver(post_delete, sender=NewsCategory)
def handle_news_category_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("news")
    revalidate_nextjs_tag("newscategories")


@receiver(post_save, sender=News)
@receiver(post_delete, sender=News)
def handle_news_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("news")
    # Also revalidate the specific news item
    revalidate_nextjs_tag(f"news-{instance.id}")


# Events models signals
@receiver(post_save, sender=EventCategory)
@receiver(post_delete, sender=EventCategory)
def handle_event_category_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("events")
    revalidate_nextjs_tag("eventcategories")


@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def handle_event_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("events")
    # Also revalidate the specific event item
    revalidate_nextjs_tag(f"event-{instance.id}")


# About models signals
@receiver(post_save, sender=Creator)
@receiver(post_delete, sender=Creator)
def handle_creator_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("creators")
    # Also revalidate the specific creator
    revalidate_nextjs_tag(f"creator-{instance.slug}")


@receiver(post_save, sender=BookCategory)
@receiver(post_delete, sender=BookCategory)
def handle_book_category_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("books")
    revalidate_nextjs_tag("bookcategories")


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def handle_book_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("books")
    # Also revalidate the specific book
    revalidate_nextjs_tag(f"book-{instance.id}")


@receiver(post_save, sender=Character)
@receiver(post_delete, sender=Character)
def handle_character_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("characters")
    # Also revalidate the specific character
    revalidate_nextjs_tag(f"character-{instance.slug}")


@receiver(post_save, sender=HistoryEvent)
@receiver(post_delete, sender=HistoryEvent)
def handle_history_event_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("history")


@receiver(post_save, sender=LicensePage)
@receiver(post_delete, sender=LicensePage)
def handle_license_page_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("about")
    revalidate_nextjs_tag("licenses")


# Home models signals
@receiver(post_save, sender=HomeSection)
@receiver(post_delete, sender=HomeSection)
def handle_home_section_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("home")
    revalidate_nextjs_tag("homesections")


@receiver(post_save, sender=HeroSlide)
@receiver(post_delete, sender=HeroSlide)
def handle_hero_slide_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("home")
    revalidate_nextjs_tag("heroslides")


# Gallery models signals
@receiver(post_save, sender=GalleryCategory)
@receiver(post_delete, sender=GalleryCategory)
def handle_gallery_category_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("gallery")
    revalidate_nextjs_tag("gallerycategories")


@receiver(post_save, sender=GalleryItem)
@receiver(post_delete, sender=GalleryItem)
def handle_gallery_item_change(sender, instance, **kwargs):
    revalidate_nextjs_tag("gallery")
    revalidate_nextjs_tag("galleryitems")
    # 개별 갤러리 아이템 태그 재검증
    revalidate_nextjs_tag(f"gallery-{instance.id}")
