from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

ROLE_NAMES = ("Super Admin", "Church Admin", "Minister")


def ensure_roles_exist():
    """
    Tests need the three Groups to exist, matching production (created
    there via `setup_groups`). We don't need real Permission objects
    attached for these tests — our role mixins check group MEMBERSHIP
    (`user.groups.filter(name=...)`), not Django's permission system,
    so plain empty groups are sufficient here.
    """
    for name in ROLE_NAMES:
        Group.objects.get_or_create(name=name)


def create_user_with_role(username, role=None, password="TestPassword123!", **extra):
    """
    Creates a test user, optionally in one of the three role groups.
    role=None returns a user with no group membership at all — useful
    for testing the "logged in but no role" boundary case.
    """
    ensure_roles_exist()
    user = User.objects.create_user(username=username, password=password, **extra)
    if role:
        user.groups.add(Group.objects.get(name=role))
    return user