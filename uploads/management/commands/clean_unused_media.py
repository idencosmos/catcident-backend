# uploads/management/commands/clean_unused_media.py
from django.core.management.base import BaseCommand
from uploads.models import Media


class Command(BaseCommand):
    help = "Deletes unused media files from the database and storage."

    def handle(self, *args, **options):
        unused = Media.objects.filter(is_used_cached=False)
        count, _ = unused.delete()
        self.stdout.write(self.style.SUCCESS(f"{count}개의 미사용 파일 삭제 완료"))