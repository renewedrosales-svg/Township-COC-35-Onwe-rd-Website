from django.test import TestCase
from django.urls import reverse

from apps.core.test_utils import create_user_with_role


class LoginTests(TestCase):
    def setUp(self):
        self.user = create_user_with_role("testadmin", role="Church Admin")

    def test_login_with_correct_credentials_succeeds(self):
        response = self.client.post(reverse("login"), {
            "username": "testadmin", "password": "TestPassword123!",
        })
        self.assertEqual(response.status_code, 302)  # redirects on success
        self.assertTrue(response.wsgi_request.user.is_authenticated) if hasattr(response, "wsgi_request") else None

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse("login"), {
            "username": "testadmin", "password": "WrongPassword!",
        })
        self.assertEqual(response.status_code, 200)  # re-renders form, not a redirect
        self.assertContains(response, "Incorrect username or password")

    def test_logout_requires_post_not_get(self):
        self.client.login(username="testadmin", password="TestPassword123!")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)  # the Phase 15 bug we already fixed live

    def test_logout_via_post_succeeds(self):
        self.client.login(username="testadmin", password="TestPassword123!")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)


class LoginLockoutTests(TestCase):
    def setUp(self):
        self.user = create_user_with_role("lockouttest", role="Minister")

    def test_five_failed_attempts_locks_out_sixth_even_correct(self):
        for _ in range(5):
            self.client.post(reverse("login"), {
                "username": "lockouttest", "password": "WrongPassword!",
            })
        response = self.client.post(reverse("login"), {
            "username": "lockouttest", "password": "TestPassword123!",  # correct this time
        })
        self.assertEqual(response.status_code, 429)

    def test_different_username_not_affected_by_others_lockout(self):
        other_user = create_user_with_role("otheruser", role="Minister")
        for _ in range(5):
            self.client.post(reverse("login"), {
                "username": "lockouttest", "password": "WrongPassword!",
            })
        # A completely different account, same client/IP, should be unaffected
        response = self.client.post(reverse("login"), {
            "username": "otheruser", "password": "TestPassword123!",
        })
        self.assertEqual(response.status_code, 302)  # succeeds normally