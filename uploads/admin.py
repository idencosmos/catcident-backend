# uploads/admin.py
from django.contrib import admin
from .models import Media
from .tasks import update_media_usage_async, clean_unused_media_async


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "file", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("title", "file")
    actions = ["update_media_usage_action", "clean_unused_media_action"]

    def update_media_usage_action(self, request, queryset):
        task = update_media_usage_async.delay()
        self.message_user(
            request, f"사용 여부 업데이트 작업이 시작되었습니다. (Task ID: {task.id})"
        )

    update_media_usage_action.short_description = "(전체, 비동기) 사용 여부 확인"

    def clean_unused_media_action(self, request, queryset):
        task = clean_unused_media_async.delay()
        self.message_user(
            request,
            f"사용 여부 확인 및 삭제 작업이 시작되었습니다. (Task ID: {task.id})",
        )

    clean_unused_media_action.short_description = (
        "(전체, 비동기) 사용 여부 확인 후 삭제"
    )
