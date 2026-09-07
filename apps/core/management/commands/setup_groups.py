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
        "church_settings.change_churchsettings",
        "church_settings.add_servicetime", "church_settings.change_servicetime", "church_settings.delete_servicetime",
        "homepage.change_homepagecontent",
        "homepage.add_creeditem", "homepage.change_creeditem", "homepage.delete_creeditem",
        "pages.add_page", "pages.change_page", "pages.delete_page",
        "pages.change_aboutpagecontent",
        "ministries.add_leader", "ministries.change_leader", "ministries.delete_leader",
        "ministries.add_ministry", "ministries.change_ministry", "ministries.delete_ministry",
    ],
    "Church Admin": [
        "church_settings.change_churchsettings",
        "church_settings.add_servicetime", "church_settings.change_servicetime", "church_settings.delete_servicetime",
        "homepage.change_homepagecontent",
        "homepage.add_creeditem", "homepage.change_creeditem", "homepage.delete_creeditem",
        "pages.add_page", "pages.change_page", "pages.delete_page",
        "pages.change_aboutpagecontent",
        "ministries.add_leader", "ministries.change_leader", "ministries.delete_leader",
        "ministries.add_ministry", "ministries.change_ministry", "ministries.delete_ministry",
        # Deliberately excludes "accounts.manage_administrators" — §7.
    ],
    "Minister": [
        # Still empty — sermons phase (7) is where this group first gets
        # real permissions (scoped to their own sermons only).
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