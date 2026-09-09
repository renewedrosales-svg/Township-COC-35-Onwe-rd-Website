from django.contrib import admin

from apps.core.audit import log_action

from .models import SchoolInfo


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    fields = (
        "school_name", "intro_text", "hero_image",
        "about_preview", "programs_preview",
        "contact_email", "contact_phone",
    )

    def has_add_permission(self, request):
        return not SchoolInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "update", obj)