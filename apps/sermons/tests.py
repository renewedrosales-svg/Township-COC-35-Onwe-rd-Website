import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Sermon

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SermonPublicVisibilityTests(TestCase):
    def test_draft_sermon_returns_404_on_public_detail(self):
        sermon = Sermon.objects.create(
            title="Unpublished Sermon", date_delivered="2026-01-01", is_published=False,
        )
        response = self.client.get(reverse("sermons:detail", args=[sermon.slug]))
        self.assertEqual(response.status_code, 404)

    def test_published_sermon_is_publicly_visible(self):
        sermon = Sermon.objects.create(
            title="Published Sermon", date_delivered="2026-01-01", is_published=True,
        )
        response = self.client.get(reverse("sermons:detail", args=[sermon.slug]))
        self.assertEqual(response.status_code, 200)

    def test_draft_sermon_not_listed_on_public_list_page(self):
        Sermon.objects.create(title="Hidden Draft", date_delivered="2026-01-01", is_published=False)
        response = self.client.get(reverse("sermons:list"))
        self.assertNotContains(response, "Hidden Draft")

    def test_slug_collision_produces_unique_slugs(self):
        s1 = Sermon.objects.create(title="Faith", date_delivered="2026-01-01")
        s2 = Sermon.objects.create(title="Faith", date_delivered="2026-02-01")
        self.assertNotEqual(s1.slug, s2.slug)
        self.assertEqual(s2.slug, "faith-2")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SermonUploadValidationTests(TestCase):
    def test_pdf_validator_rejects_fake_pdf(self):
        fake_pdf = SimpleUploadedFile("notes.pdf", b"this is not really a pdf", content_type="application/pdf")
        sermon = Sermon(title="Test", date_delivered="2026-01-01", notes_pdf=fake_pdf)
        with self.assertRaises(Exception):
            sermon.full_clean()

    def test_pdf_validator_accepts_real_pdf_header(self):
        real_pdf_bytes = b"%PDF-1.4\n%fake but valid header\n"
        real_pdf = SimpleUploadedFile("notes.pdf", real_pdf_bytes, content_type="application/pdf")
        sermon = Sermon(title="Test", date_delivered="2026-01-01", notes_pdf=real_pdf)
        try:
            sermon.full_clean()
        except Exception as e:
            self.fail(f"Valid PDF header was incorrectly rejected: {e}")