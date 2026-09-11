from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Page

class ContactFormSecurityTests(TestCase):
    def setUp(self):
        cache.clear()  # each test starts with a clean rate-limit slate

    def test_valid_submission_creates_message(self):
        response = self.client.post(reverse("pages:contact"), {
            "name": "Jane Doe", "email": "jane@example.com",
            "subject": "Hello", "message": "A real message.",
            "website": "",  # honeypot left empty, as a real user would
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email="jane@example.com").exists())

    def test_honeypot_filled_in_rejects_submission(self):
        response = self.client.post(reverse("pages:contact"), {
            "name": "Bot", "email": "bot@example.com",
            "subject": "Spam", "message": "Buy this now.",
            "website": "http://spam.example.com",  # a bot fills this in
        })
        self.assertFalse(ContactMessage.objects.filter(email="bot@example.com").exists())

    def test_csrf_protection_enforced(self):
        csrf_client = self.client_class(enforce_csrf_checks=True)
        response = csrf_client.post(reverse("pages:contact"), {
            "name": "Jane", "email": "jane@example.com",
            "subject": "Hi", "message": "Test", "website": "",
        })
        self.assertEqual(response.status_code, 403)  # rejected without a valid CSRF token

    def test_sixth_rapid_submission_returns_429(self):
        for i in range(5):
            self.client.post(reverse("pages:contact"), {
                "name": "Jane", "email": f"jane{i}@example.com",
                "subject": "Hi", "message": "Test", "website": "",
            })
        response = self.client.post(reverse("pages:contact"), {
            "name": "Jane", "email": "jane6@example.com",
            "subject": "Hi", "message": "Test", "website": "",
        })
        self.assertEqual(response.status_code, 429)


class ReservedSlugTests(TestCase):
    def test_reserved_slug_rejected_on_save(self):
        page = Page(title="Admin Page", slug="admin", body="Content")
        with self.assertRaises(Exception):
            page.save()

    def test_ordinary_slug_accepted(self):
        page = Page(title="Our Faith", slug="our-faith", body="Content", is_published=True)
        page.save()  # should not raise
        self.assertTrue(Page.objects.filter(slug="our-faith").exists())