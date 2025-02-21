# uploads/tests.py
from django.test import TestCase
from django.apps import apps
from .models import Media
from homepage.models.events_models import Event, EventCategory


class MediaUsageTestCase(TestCase):
    def setUp(self):
        self.media = Media.objects.create(file='test.jpg', title='Test Media')
        self.category = EventCategory.objects.create(slug='test-cat')
        self.event = Event.objects.create(
            category=self.category,
            main_image=self.media,
            date='2025-01-01'
        )

    def test_media_used(self):
        self.assertTrue(self.media.is_used_cached)
        self.assertEqual(len(self.media.get_usage_details()), 1)

    def test_media_unused_after_change(self):
        new_media = Media.objects.create(file='new.jpg', title='New Media')
        self.event.main_image = new_media
        self.event.save()
        self.assertFalse(self.media.is_used_cached)
        self.assertTrue(new_media.is_used_cached)

    def test_media_unused_after_delete(self):
        self.event.delete()
        self.assertFalse(self.media.is_used_cached)