from django.test import TestCase
from django.urls import reverse

from apps.core.test_utils import create_user_with_role
from apps.sermons.models import Sermon


class RoleBasedAccessTests(TestCase):
    def setUp(self):
        self.super_admin = create_user_with_role("superadmin", role="Super Admin")
        self.church_admin = create_user_with_role("churchadmin", role="Church Admin")
        self.minister = create_user_with_role("minister", role="Minister")
        self.no_role_user = create_user_with_role("norole", role=None)

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_no_role_user_gets_403_not_redirect(self):
        self.client.login(username="norole", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 403)

    def test_minister_blocked_from_church_admin_only_view(self):
        self.client.login(username="minister", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:page_list"))
        self.assertEqual(response.status_code, 403)

    def test_church_admin_allowed_into_church_admin_view(self):
        self.client.login(username="churchadmin", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:page_list"))
        self.assertEqual(response.status_code, 200)

    def test_super_admin_allowed_into_super_admin_only_view(self):
        self.client.login(username="superadmin", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:church_settings"))
        self.assertEqual(response.status_code, 200)

    def test_church_admin_blocked_from_support_page_settings(self):
        # Support content editing is deliberately Super-Admin-only (Phase 11)
        self.client.login(username="churchadmin", password="TestPassword123!")
        # There's no dedicated dashboard view for Support content (it's
        # /admin/ only per Phase 11), so this verifies the underlying
        # permission grant directly instead.
        self.church_admin.refresh_from_db()
        self.assertFalse(self.church_admin.has_perm("pages.change_supportpagecontent"))


class MinisterOwnershipTests(TestCase):
    """
    The actual point of OwnerOrElevatedRequiredMixin /
    MinisterOwnershipRequiredMixin (Phase 3 + Phase 12) — a Minister
    may only edit/delete their OWN sermons, enforced server-side.
    """

    def setUp(self):
        self.minister_a = create_user_with_role("ministera", role="Minister")
        self.minister_b = create_user_with_role("ministerb", role="Minister")
        self.church_admin = create_user_with_role("churchadmin2", role="Church Admin")

        self.sermon_a = Sermon.objects.create(
            title="Sermon by A", date_delivered="2026-01-01", created_by=self.minister_a,
        )

    def test_minister_can_edit_own_sermon(self):
        self.client.login(username="ministera", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:sermon_update", args=[self.sermon_a.slug]))
        self.assertEqual(response.status_code, 200)

    def test_minister_cannot_edit_another_ministers_sermon(self):
        self.client.login(username="ministerb", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:sermon_update", args=[self.sermon_a.slug]))
        self.assertEqual(response.status_code, 403)

    def test_minister_cannot_delete_another_ministers_sermon(self):
        self.client.login(username="ministerb", password="TestPassword123!")
        response = self.client.post(reverse("dashboard:sermon_delete", args=[self.sermon_a.slug]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Sermon.objects.filter(pk=self.sermon_a.pk).exists())  # confirms it wasn't deleted anyway

    def test_church_admin_can_edit_any_ministers_sermon(self):
        self.client.login(username="churchadmin2", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:sermon_update", args=[self.sermon_a.slug]))
        self.assertEqual(response.status_code, 200)

    def test_minister_list_view_shows_only_own_sermons(self):
        Sermon.objects.create(title="Sermon by B", date_delivered="2026-01-02", created_by=self.minister_b)
        self.client.login(username="ministera", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:sermon_list"))
        self.assertContains(response, "Sermon by A")
        self.assertNotContains(response, "Sermon by B")