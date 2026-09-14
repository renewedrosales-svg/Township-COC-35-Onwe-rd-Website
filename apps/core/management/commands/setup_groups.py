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
        "sermons.add_sermoncategory", "sermons.change_sermoncategory", "sermons.delete_sermoncategory",
        "sermons.add_sermon", "sermons.change_sermon", "sermons.delete_sermon",
        "events.add_event", "events.change_event", "events.delete_event", "news.add_newscategory", "news.change_newscategory", "news.delete_newscategory",
        "news.add_article", "news.change_article", "news.delete_article",
        "gallery.add_galleryphoto", "gallery.change_galleryphoto", "gallery.delete_galleryphoto",
        "pages.change_contactmessage", "pages.delete_contactmessage",
        "pages.change_supportpagecontent",
        "pages.add_bankaccount", "pages.change_bankaccount", "pages.delete_bankaccount",
        "school.change_schoolinfo",
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
        "sermons.add_sermoncategory", "sermons.change_sermoncategory", "sermons.delete_sermoncategory",
        "sermons.add_sermon", "sermons.change_sermon", "sermons.delete_sermon",
        "events.add_event", "events.change_event", "events.delete_event", "news.add_newscategory", "news.change_newscategory", "news.delete_newscategory",
        "news.add_article", "news.change_article", "news.delete_article",
        "gallery.add_galleryphoto", "gallery.change_galleryphoto", "gallery.delete_galleryphoto",
        "pages.change_contactmessage", "pages.delete_contactmessage",
    ],

    "Minister": [
        # Ministers CAN add/change/delete sermons at the permission
        # level — the restriction to "their own only" is enforced by
        # OwnerOrElevatedRequiredMixin / admin get_queryset above, not
        # by Django's permission system (which can't express per-object
        # ownership, as noted back in Phase 3 Step 2).
        "sermons.add_sermon", "sermons.change_sermon", "sermons.delete_sermon",
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