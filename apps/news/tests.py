from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article


class ScheduledPublicationTests(TestCase):
    def test_future_scheduled_article_not_publicly_visible(self):
        article = Article.objects.create(
            title="Future Article",
            body="Content",
            status=Article.Status.PUBLISHED,
            publish_date=timezone.now() + timedelta(hours=2),
        )
        response = self.client.get(reverse("news:detail", args=[article.slug]))
        self.assertEqual(response.status_code, 404)

    def test_past_scheduled_published_article_is_visible(self):
        article = Article.objects.create(
            title="Past Article",
            body="Content",
            status=Article.Status.PUBLISHED,
            publish_date=timezone.now() - timedelta(hours=2),
        )
        response = self.client.get(reverse("news:detail", args=[article.slug]))
        self.assertEqual(response.status_code, 200)

    def test_draft_article_not_publicly_visible_regardless_of_date(self):
        article = Article.objects.create(
            title="Draft Article",
            body="Content",
            status=Article.Status.DRAFT,
            publish_date=timezone.now() - timedelta(hours=2),  # date has passed, but status is draft
        )
        response = self.client.get(reverse("news:detail", args=[article.slug]))
        self.assertEqual(response.status_code, 404)

    def test_archived_article_not_publicly_visible(self):
        article = Article.objects.create(
            title="Archived Article",
            body="Content",
            status=Article.Status.ARCHIVED,
            publish_date=timezone.now() - timedelta(days=30),
        )
        response = self.client.get(reverse("news:detail", args=[article.slug]))
        self.assertEqual(response.status_code, 404)

    def test_homepage_does_not_leak_scheduled_article(self):
        # This specifically re-verifies the discipline from Phase 14:
        # the homepage preview must use .public() too, not just the
        # dedicated news list view.
        Article.objects.create(
            title="Should Not Appear Yet",
            body="Content",
            status=Article.Status.PUBLISHED,
            publish_date=timezone.now() + timedelta(hours=2),
        )
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Should Not Appear Yet")