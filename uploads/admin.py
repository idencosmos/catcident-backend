# uploads/admin.py
from django.contrib import admin
from .models import Media


class IsUsedFilter(admin.SimpleListFilter):
    title = '사용 여부'
    parameter_name = 'is_used'

    def lookups(self, request, model_admin):
        return (
            ('yes', '사용 중'),
            ('no', '미사용'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_used_cached=True)
        if self.value() == 'no':
            return queryset.filter(is_used_cached=False)
        return queryset


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'uploaded_at', 'is_used_display', 'usage_summary')
    list_filter = ('uploaded_at', IsUsedFilter)
    search_fields = ('title', 'file')
    actions = ['delete_unused_media']

    def is_used_display(self, obj):
        return obj.is_used_cached
    is_used_display.boolean = True
    is_used_display.short_description = '사용 여부'

    def usage_summary(self, obj):
        usage = obj.get_usage_details()
        if not usage:
            return "미사용"
        return ", ".join([f"{u['model']} ({u['count']}건)" for u in usage])
    usage_summary.short_description = '사용처'

    def delete_unused_media(self, request, queryset):
        unused = queryset.filter(is_used_cached=False)
        count, _ = unused.delete()
        self.message_user(request, f"{count}개의 미사용 파일이 삭제되었습니다.")
    delete_unused_media.short_description = "선택된 미사용 파일 삭제"