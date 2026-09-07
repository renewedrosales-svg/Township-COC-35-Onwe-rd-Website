from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the 35 Onwe Road Church of Christ CMS.

    Role assignment (Super Admin / Church Admin / Minister) is handled
    through Django Groups + Permissions, not a hardcoded role field.
    This keeps authorization enforcement server-side and extensible —
    a new role can be added later via Groups without a schema change.

    The three convenience properties below are for DISPLAY purposes
    only (e.g. showing a role badge in the dashboard nav). They must
    NEVER be used as the actual authorization check in a view — views
    use permission_required/PermissionRequiredMixin against real
    Django permissions, built in the next step.
    """

    class Meta:
        db_table = "accounts_user"
        permissions = [
            ("manage_administrators", "Can manage church administrators and their roles"),
        ]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_super_admin(self):
        return self.groups.filter(name="Super Admin").exists()

    @property
    def is_church_admin(self):
        return self.groups.filter(name="Church Admin").exists()

    @property
    def is_minister(self):
        return self.groups.filter(name="Minister").exists()