from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


# Single source of truth for RBAC group assignments.
#
# Format: { group_name: [ "app_label.codename", ... ] }
#
# As each content app (sermons, events, news, ...) gets its models built
# in later phases, add its permission codenames to the relevant group(s)
# here, then re-run: python manage.py setup_groups
#
# Any codename listed here that doesn't exist yet (because its app has
# no models yet) is skipped with a warning, not a crash — this lets the
# command stay accurate as the single RBAC reference even mid-project.
GROUP_PERMISSIONS = {
    "Super Admin": [
        "accounts.manage_administrators",
        # Content permissions accumulate here as each app is built:
        # "church_settings.change_churchsettings",
        # "homepage.add_homepagesection", "homepage.change_homepagesection", ...
        # "sermons.add_sermon", "sermons.change_sermon", "sermons.delete_sermon", ...
        # (Super Admin gets full CRUD on everything — added incrementally below
        #  as models are created; Church Admin's list mirrors most of these
        #  minus system-level entries.)
    ],
    "Church Admin": [
        # Populated starting with the church_settings/homepage/pages phases.
        # Deliberately does NOT include "accounts.manage_administrators" —
        # per spec (§7), Church Admins never get system-level authority
        # even though they manage day-to-day content.
    ],
    "Minister": [
        # Populated starting with the sermons phase.
        # Ministers get "sermons.add_sermon" / "change_sermon" (can act on
        # sermons at all) — ownership restriction to "their own sermons
        # only" happens in view logic, not here, as explained above.
    ],
}


class Command(BaseCommand):
    help = "Creates or updates the Super Admin, Church Admin, and Minister groups and their permissions."

    def handle(self, *args, **options):
        for group_name, codenames in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            status = "Created" if created else "Found existing"
            self.stdout.write(f"{status} group: {group_name}")

            resolved_permissions = []
            for codename_ref in codenames:
                app_label, codename = codename_ref.split(".")
                try:
                    permission = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    resolved_permissions.append(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Skipped '{codename_ref}' — model/permission doesn't exist yet. "
                            f"This is expected if that app hasn't been built yet."
                        )
                    )

            group.permissions.set(resolved_permissions)
            self.stdout.write(f"  Assigned {len(resolved_permissions)} permission(s).")

        self.stdout.write(self.style.SUCCESS("Group setup complete."))